import { Link } from "react-router";
import Button from "./Button"
import { CgHome } from "react-icons/cg";
import { CgPlayListCheck } from "react-icons/cg";
import { CgChart } from "react-icons/cg";
import { CgLogOut } from "react-icons/cg";
import { FaVideo } from "react-icons/fa";
import { FaGear } from "react-icons/fa6";

function Sidebar() {
  return (
    <div className="w-20 px-2 py-3 bg-neutral-700/50">
        <nav className="w-full h-full flex flex-col justify-between items-center">
            <div className="flex flex-col items-center">
              <img className="w-full rounded-md" src="./src/assets/Meet_Up_Logo.jpg" alt="MeetUp Logo"/>
              <Button className="w-[80%] h-12.5 mt-3 rounded-md bg-[#0c0c0c] flex justify-center items-center transition-normal duration-200 hover:w-[90%] hover:h-14 hover:mt-1.5"><CgHome color={"white"} size={30}/></Button>
              <Button className="w-[80%] h-12.5 mt-3 rounded-md bg-[#0c0c0c] flex justify-center items-center transition-normal duration-200 hover:w-[90%] hover:h-14 hover:mt-1.5"><FaVideo color={"white"} size={30}/></Button>
              <Button className="w-[80%] h-12.5 mt-3 rounded-md bg-[#0c0c0c] flex justify-center items-center transition-normal duration-200 hover:w-[90%] hover:h-14 hover:mt-1.5"><CgPlayListCheck color={"white"} size={30}/></Button>
              <Button className="w-[80%] h-12.5 mt-3 rounded-md bg-[#0c0c0c] flex justify-center items-center transition-normal duration-200 hover:w-[90%] hover:h-14 hover:mt-1.5"><CgChart color={"white"} size={30}/></Button>
              <Button className="w-[80%] h-12.5 mt-3 rounded-md bg-[#0c0c0c] flex justify-center items-center transition-normal duration-200 hover:w-[90%] hover:h-14 hover:mt-1.5"><FaGear color={"white"} size={30}/></Button>
            </div>
            <Link to="/" className="w-[80%] h-12.5 rounded-md bg-[#0c0c0c] flex justify-center items-center">
              <Button className="cursor-pointer"><CgLogOut color={"white"} size={30}/></Button>
            </Link>
        </nav>
    </div>
  )
}

export default Sidebar