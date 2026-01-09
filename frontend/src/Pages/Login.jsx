import { useState } from "react";
import { Link, useNavigate } from "react-router";
import api from "../api/backend_api";

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async () => {
        try {
        const formData = new URLSearchParams();
        formData.append("username", email); // OAuth2PasswordRequestForm expects "username"
        formData.append("password", password);

        const res = await api.post("/auth/login", formData, {
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            }
        });

        localStorage.setItem("access_token", res.data.access_token);
        navigate("/myhome");
        } catch (err) {
        setError("Invalid email or password");
        }
    };

  return (
    <div className="w-screen min-h-screen flex justify-center items-center bg-linear-0 from-[#2b2b2b] to-[#0c0c0c]">
        <img className="absolute w-80 bottom-5 left-12 hidden md:block" src="./src/assets/image.png" alt="image" />
        <div className="w-[70%] md:w-[30%] min-h-150 md:min-h-170 px-5 py-5 flex flex-col rounded-4xl bg-white">
            <span className="text-2xl font-[Silkscreen] mb-3">MEETUP</span>
            <div className="font-[Poppins]">
                <div className="my-5 md:my-10">
                    <h1 className="text-center text-5xl md:text-6xl font-extrabold">Hi there,</h1>
                    <h1 className="text-center text-md md:text-xl">Welcome to MeetUp</h1>
                </div>
                <div className="flex flex-col justify-evenly items-center">
                    <input type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-60 md:w-80 h-10 mt-5 px-3 py-1.5 bg-gray-100 rounded-xl outline-1"/>
                    <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-60 md:w-80 h-10 mt-5 px-3 py-1.5 bg-gray-100 rounded-xl outline-1"/>
                    <div className="w-60 md:w-80 mt-3 text-right text-sm md:text-md text-red-500 cursor-pointer">
                        <Link to="forgot_password">Forgot Password?</Link>
                    </div>
                    <div className="w-60 md:w-80 my-6 outline-1"></div>
                    {error && <p className="mt-3 text-red-500">{error}</p>}
                    {/* <Link to="/myhome">
                        <button className="w-60 md:w-80 my-2 py-2 flex justify-center items-center bg-gray-100 md:text-xl rounded-xl outline-1 cursor-pointer transition-colors hover:bg-gray-200">
                            <span>Login with Google</span>
                            <img className="w-6 h-6 mx-2" src="./src/assets/google_logo.png" alt="google_logo" />
                        </button>
                    </Link> */}
                    <Link to="/myhome">
                        <button onClick={handleLogin} className="w-60 md:w-80 my-2 py-2 flex justify-center items-center bg-[#FFDD22] md:text-xl font-bold rounded-xl cursor-pointer transition-colors hover:bg-amber-300">
                            <span>Login</span>
                        </button>
                    </Link>
                    <div className="my-2 text-sm md:text-md">
                        Don't have an Account?
                        <Link to="/signup" className="mx-2 text-red-500 cursor-pointer">
                            Sign up
                        </Link>
                    </div>
                </div>
            </div>
        </div>
        <img className="absolute w-80 top-5 right-0 hidden md:block" src="./src/assets/image.png" alt="image" />
    </div>
  )
}

export default Login