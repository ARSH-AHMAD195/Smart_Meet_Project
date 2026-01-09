import { Outlet } from "react-router";
import Sidebar from "../Components/UI/Sidebar";

export default function MyHomeLayout() {
  return (
    <div className="w-screen h-screen bg-[#0c0c0c] flex">
      <Sidebar/>
      <div>
        <Outlet />
      </div>
    </div>
  );
}
