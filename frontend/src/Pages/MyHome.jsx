import { useEffect, useState } from "react";
import MeetCard from "../Components/UI/MeetCard";
import api from "../api/backend_api";
import { formatDate, formatTime, formatActionItems } from "../utils/utils";

function MyHome() {
  
  const [summary, setSummary] = useState()
  const [title, setTitle] = useState()
  const [date, setDate] = useState()
  const [actionItems, setActionItems] = useState([]);

  const getSummary = async (meeting_id) => {
    try {
      const res = await api.get(`/meets/${meeting_id}/summary`);
      console.log(res.data.summary)
      setSummary(res.data.summary)
    } catch (error) {
      console.log(error)
    }
  };

  const getMeetingDetails = async (meeting_id) => {
    try {
      const res = await api.get(`/meets/${meeting_id}`)
      console.log(res.data)
      setTitle(res.data.topic)
      setDate(res.data.date)
    } catch (error) {
      console.log(error)
    }
  };

  useEffect(() => {
    getSummary(1)
    getMeetingDetails(1)
  } , [])

  const getActionItem = async (meeting_id) => {
      try {
      const res = await api.get(`/meets/${meeting_id}/action-items`);

      const formattedItems = formatActionItems(res.data.action_items)
      setActionItems(formattedItems)
      console.log("Parent actionItems:", actionItems);
      } catch (error) {
      console.log(error)
      }
  };

  useEffect(() => {
      getActionItem(1)
  },[])

  return (
    <div className="w-[calc(100vw-80px)] md:h-full bg-[#0c0c0c] font-[Poppins]">
      <div className="md:w-[70%] h-full px-3 md:px-10 py-3 md:py-10 bg-[#0c0c0c]/20 flex flex-col justify-between">
        <div className="w-full flex flex-col justify-between bg-[#0c0c0c]/30">
          <div className="px-3 py-3">
            <span className="text-[#FFDD22] text-4xl font-bold">New </span>
            <span className="text-white text-4xl font-bold">Meeting</span>
          </div>
          <div className="px-3 py-3 bg-neutral-800 rounded-lg">
            <div className="px-3 py-3 flex justify-between">
              <input className="w-[70%] h-12 rounded-md px-5 bg-white" type="text" placeholder="Type code or link to join" />
              <button className="w-30 h-12 ml-5 font-bold rounded-md bg-[#FFDD22]">Join</button>
            </div>
          </div>
        </div>
        <div className="w-full mt-10 flex flex-col justify-between bg-[#0c0c0c]/30">
          <div className="px-3 py-3">
            <span className="text-[#FFDD22] text-4xl font-bold">Recent </span>
            <span className="text-white text-4xl font-bold">Meetings</span>
          </div>
          <div className="w-full h-full px-3 py-3 rounded-lg">
            <div className="w-full h-full px-2 md:px-3 py-3 grid grid-cols-1 md:grid-cols-3 gap-5">
              <MeetCard Title={title} Desc={"Client meeting discussion on the requirements."} Date={formatDate(date)} Time={formatTime(date)} Image={"./src/assets/ms_teams.png"} Summary={summary} ActionItems={actionItems}/>
              <MeetCard Title={"Feature Launch"} Desc={"Team meeting discussion on the new feature launch."} Date={"Dec 12, 2025"} Time={"45 Mins"} Image={"./src/assets/ms_teams.png"}/>
              <MeetCard Title={"Bug Fix"} Desc={"Team meeting discussion on the bug fixes."} Date={"Dec 12, 2025"} Time={"32 Mins"} Image={"./src/assets/g_meet.png"}/>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MyHome