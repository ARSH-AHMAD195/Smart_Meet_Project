import { Route, Routes } from "react-router"
import Home from "./Pages/Home"
import MyHome from "./Pages/MyHome"
import LandingLayout from "./Layouts/LandingLayout"
import LoginLayout from "./Layouts/LoginLayout"
import MyHomeLayout from "./Layouts/MyHomeLayout"
import ProtectedRoute from "./Components/ProtectedRoute"

function App() {
  return (
    <Routes>
      <Route element={<LandingLayout/>}>
        <Route path="/" element={<Home/>} />
      </Route>
      <Route path="/signin" element={<LoginLayout/>}/>
      <Route element={
        <ProtectedRoute>
            <MyHomeLayout/>
        </ProtectedRoute>
        }>
        <Route path="/myhome" element={<MyHome/>}/>
      </Route>
    </Routes>
  )
}

export default App
