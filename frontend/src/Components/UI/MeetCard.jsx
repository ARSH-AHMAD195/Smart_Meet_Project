import { useState } from "react";
import { FaRegCalendarAlt } from "react-icons/fa";
import { FaRegClock } from "react-icons/fa";
import { FaListUl } from "react-icons/fa";
import Modal from "./Modal";
import ActionItemList from "./ActionItemList";

function MeetCard({Title, Date, Time, Image, Desc, Summary, ActionItems}) {
    const [open, setOpen] = useState(false);
    console.log("MeetCard ActionItems:", ActionItems);

   
  return (
    <div>
        <div className="md:w-95 md:h-110 px-10 py-10 flex flex-col justify-between bg-neutral-800 text-white rounded-3xl">
            <div>
                <h1 className="text-2xl md:text-3xl font-bold">{Title}</h1>
                <div className="pt-1 flex justify-between items-center md:text-md">
                    <div className="flex justify-center items-center">
                        <FaRegCalendarAlt size={20}/>
                        <span className="ml-3">{Date}</span>
                    </div>
                    <div className="h-6 w-0 outline-1"></div>
                    <div className="flex justify-center items-center">
                        <FaRegClock size={20}/>
                        <span className="ml-3">{Time}</span>
                    </div>
                    <div className="h-6 w-0 outline-1"></div>
                    <div className="w-8 h-8">
                        <img src={Image} alt="Meet_Logo" />
                    </div>
                </div>
                <p className="pt-10 text-sm md:text-lg">
                    {Desc}
                </p>
            </div>
            <div>
                <button className="mt-2 px-5 py-5 flex justify-start items-center rounded-2xl bg-white/30 cursor-pointer" onClick={() => {setOpen(true)}}>
                    <FaListUl size={25}/>
                    <span className="px-5 text-sm md:text-2xl">Meet Summary</span>
                </button>
                <Modal open={open}>
                    <h1 className="text-black text-5xl font-bold">Meet Summary</h1>
                    <h1 className="mt-5 text-black text-2xl font-bold flex justify-center items-center">
                        {Title}
                        <span className="px-3">|</span>
                        <FaRegCalendarAlt size={25}/>
                        <span className="ml-3">{Date}</span>
                        <span className="px-3">|</span>
                        <FaRegClock size={20}/>
                        <span className="ml-3">{Time}</span>
                        <span className="px-3">|</span>
                        <img src={Image} className="w-8 h-8" alt="Meet_Logo" />
                    </h1>
                    <p className="mt-5 px-10 text-justify text-black text-xl">{Summary}</p>
                    <ActionItemList items={ActionItems}/>
                    <button onClick={() => {setOpen(false)}} className="mt-5 px-6 py-3 outline-2 text-black text-2xl font-semibold rounded-xl transition-colors cursor-pointer hover:bg-black hover:text-white">Close</button>
                </Modal>
            </div>
        </div>
    </div>
  )
}

export default MeetCard