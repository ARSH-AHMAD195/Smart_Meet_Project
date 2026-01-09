import Header from "../Components/Header";
import { Outlet } from "react-router";

export default function LandingLayout() {
  return (
    <div>
      <Header />
      <div>
        <Outlet />
      </div>
    </div>
  );
}
