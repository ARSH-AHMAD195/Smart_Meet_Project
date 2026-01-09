from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass
from App.models.model import ActionItem
from google import genai
import uuid

import heapq
import logging

from App.core.config import setting

logger = logging.getLogger("ai_service")
logger.setLevel(logging.DEBUG)

class ActionItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    assignee: Optional[str] = None
    due_date: Optional[str] = None  # ISO date string if available
    confidence: Optional[float] = None

class SummarizationResult(BaseModel):
    summary: str
    action_items: List[ActionItem]
    metadata: Dict[str, Any] = {}

class BaseLLM:
    def generate(self, prompt:str, **kwargs) -> str:
        raise NotImplementedError
    
class GeminiLLM(BaseLLM):
    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        self.api_key = setting.get_gemini_api_key()
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return getattr(response, "text", "").strip() 
    

class BaseEmbedding:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError
    
class GeminiEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = "text-embedding-004"):
        self.api_key = setting.get_gemini_api_key()
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        vectors = []
        for text in texts:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=text,
            )
            vectors.append(result.embeddings)
        return vectors
    
@dataclass
class VectorRecord:
    id: str
    text: str
    vector: List[float]
    metadata: Dict[str, Any]

class VectorStore:
    def add_documents(self, docs: List[VectorRecord]):
        raise NotImplementedError
    def search(self, query_vector: List[float], top_k: int=5) -> List[VectorRecord]:
        raise NotImplementedError
    def get_by_ids(self, ids: List[str]) -> List[VectorRecord]:
        raise NotImplementedError
    def clear(self):
        raise NotImplementedError

class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self._records: List[VectorRecord] = []

    def add_documents(self, docs: List[VectorRecord]):
        logger.debug("Adding %d documents to vector store", len(docs))
        self._records.extend(docs)

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        # assumes already normalized vectors where possible
        return sum(x*y for x, y in zip(a, b))

    def search(self, query_vector: List[float], top_k: int=5) -> List[VectorRecord]:
        heap: List[Tuple[float, VectorRecord]] = []
        for r in self._records:
            sim = self._cosine_similarity(query_vector, r.vector)
            if len(heap) < top_k:
                heapq.heappush(heap, (sim, r))
            else:
                if sim > heap[0][0]:
                    heapq.heapreplace(heap, (sim, r))
        # return sorted by descending score
        results = sorted(heap, key=lambda x: x[0], reverse=True)
        return [r for score, r in results]

    def get_by_ids(self, ids: List[str]) -> List[VectorRecord]:
        return [r for r in self._records if r.id in ids]
    
    def clear(self):
        self._records = []

class RAGService:
    def __init__(self,
                 llm: BaseLLM,
                 embedder: BaseEmbedding,
                 vectorstore: Optional[VectorStore] = None,
                 chunk_size: int = 800,
                 chunk_overlap: int = 100):
        self.llm = llm
        self.embedder = embedder
        self.store = vectorstore or InMemoryVectorStore()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # map transcript_id -> list of records ids (optional)
        self._index_map: Dict[str, List[str]] = {}

    # --------- indexing pipeline ----------
    def _chunk_text(self, text: str) -> List[str]:
        # simple whitespace chunking. In production, use sentence splitting + smart overlap.
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(" ".join(chunk_words))
            i += self.chunk_size - self.chunk_overlap
        logger.debug("Chunked text into %d pieces", len(chunks))
        return chunks

    def index_transcript(self, transcript_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        metadata = metadata or {}
        chunks = self._chunk_text(text)
        vectors = self.embedder.embed_texts(chunks)
        records = []
        ids = []
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            rec = VectorRecord(id=f"{transcript_id}::chunk::{i}", text=chunk, vector=vec, metadata={**metadata, "chunk_index": i})
            records.append(rec)
            ids.append(rec.id)
        self.store.add_documents(records)
        self._index_map[transcript_id] = ids
        logger.info("Indexed transcript %s with %d chunks", transcript_id, len(chunks))

    # --------- retrieval ----------
    def retrieve(self, query: str, top_k: int = 4) -> List[VectorRecord]:
        qvecs = self.embedder.embed_texts([query])
        qvec = qvecs[0]
        hits = self.store.search(qvec, top_k=top_k)
        logger.debug("Retrieved %d hits for query", len(hits))
        return hits

    # --------- high-level operations ----------
    def summarize_transcript(self, transcript_id: str, max_context_chunks: int = 6) -> SummarizationResult:
        # find transcript chunks by id list
        ids = self._index_map.get(transcript_id)
        if not ids:
            raise ValueError("Transcript not indexed: %s" % transcript_id)
        # retrieve top chunks by dummy query 'summarize' — in production, score by recency/importance
        # for demo: just pick first N
        chosen_records = self.store.get_by_ids(ids)[:max_context_chunks]
        combined = "\n\n".join(r.text for r in chosen_records)

        # Summarize
        summary_prompt = self._build_summary_prompt(combined)
        summary_text = self.llm.generate(summary_prompt, max_tokens=150, temperature=0.0)

        # Extract action items — use a dedicated prompt
        action_prompt = self._build_action_prompt(combined)
        actions_text = self.llm.generate(action_prompt, max_tokens=120, temperature=0.0)
        action_items = self._parse_action_items(actions_text)

        result = SummarizationResult(summary=summary_text.strip(), action_items=action_items,
                                     metadata={"transcript_id": transcript_id})
        return result

    def query_and_answer(self, query: str, top_k: int = 4, max_answer_tokens: int = 128) -> str:
        hits = self.retrieve(query, top_k=top_k)
        context = "\n\n".join([h.text for h in hits])
        prompt = f"Use the following meeting transcript excerpts to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer concisely."
        return self.llm.generate(prompt, max_tokens=max_answer_tokens, temperature=0.0)

    # --------- prompts & parsing ----------
    def _build_summary_prompt(self, context: str) -> str:
        return (
            "You are an assistant that produces concise, factual meeting summaries.\n"
            "Produce: (1) a short executive summary (2-4 sentences), (2) 2-6 bullet highlights.\n"
            "Context:\n"
            f"{context}\n\n"
            "Output format:\nEXECUTIVE SUMMARY:\n- <one paragraph>\nHIGHLIGHTS:\n- <bullet>\n- <bullet>\n"
        )

    def _build_action_prompt(self, context: str) -> str:
        return (
            "**Task:** Extract distinct action items from the provided Context. "
            "For each action item, strictly output a single line using the following semicolon-separated format:\n"
            "**Action Description; Assignee: [Name or Unassigned]; Due: [Date or TBD]**\n\n"
            "**Formatting Rules:**\n"
            "* The description must be first. And description must only tell assigned task.\n"
            "* Use the exact prefixes **'Assignee:'** and **'Due:'** (or **'Due date:'**) for the metadata.\n"
            "* If the assignee is not explicitly mentioned, use **'Assignee: Unassigned'**.\n"
            "* If no due date is mentioned, use **'Due: TBD'**.\n"
            "* Return ONLY the list of action item lines, without any introductory text, numbering, or bullet points.\n\n"
            f"**Context:**\n{context}\n"
        )

    def _parse_action_items(self, raw: str) -> List[ActionItem]:
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        items: List[ActionItem] = []
        for ln in lines:
            # Basic parse strategy: split by ';' or ' - ' or '|' or parentheses
            desc = ln
            assignee = None
            due = None
            # heuristics
            if ';' in ln:
                parts = [p.strip() for p in ln.split(';')]
                desc = parts[0]
                for p in parts[1:]:
                    if p.lower().startswith('assignee:'):
                        assignee = p.split(':', 1)[1].strip()
                    elif p.lower().startswith('due:') or p.lower().startswith('due date:'):
                        due = p.split(':', 1)[1].strip()
            else:
                # look for parentheses like (Assignee: Bob, Due: 2025-11-05)
                if '(' in ln and ')' in ln:
                    start = ln.find('(')
                    desc = ln[:start].strip(' -\t')
                    meta = ln[start+1:ln.find(')')]
                    for p in meta.split(','):
                        if 'assignee' in p.lower():
                            assignee = p.split(':', 1)[1].strip()
                        if 'due' in p.lower():
                            due = p.split(':', 1)[1].strip()
            ai = ActionItem(description=desc, assignee=assignee or 'Unassigned', due_date=due, confidence=None)
            items.append(ai)
        return items