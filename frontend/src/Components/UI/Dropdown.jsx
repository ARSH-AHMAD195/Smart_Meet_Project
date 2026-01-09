import { useState, useRef, useEffect } from "react";
import { Link } from "react-router";
import { SlArrowDown, SlArrowUp } from "react-icons/sl";

export default function Dropdown() {
    const [open, setOpen] = useState(false);
    const ref = useRef(null);

    // Close dropdown on outside click
    useEffect(() => {
        const handleClick = (e) => {
            if (ref.current && !ref.current.contains(e.target)) {
                setOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);

    return (
        <div ref={ref} className="relative text-white font-[Silkscreen]">
            {/* Button */}
            <button
                onClick={() => setOpen(!open)}
                className="px-6 py-3 w-48 border border-white rounded-xl flex justify-evenly items-center space-x-2 cursor-pointer hover:text-[#FFDD33]"
            >
                <span>MEET</span>
                {open ? <SlArrowUp size={20} /> : <SlArrowDown size={20} />}
            </button>

            {/* Dropdown panel */}
            {open && (
                <div className="absolute left-0 mt-2 w-48 bg-white text-black text-sm rounded-xl shadow-lg py-3 z-50">
                    <Link
                        to="/meet/join"
                        className="block px-5 py-2 hover:bg-gray-100 rounded-md"
                        onClick={() => setOpen(false)}
                    >
                        Join Meeting
                    </Link>

                    <Link
                        to="/meet/host"
                        className="block px-5 py-2 hover:bg-gray-100 rounded-md"
                        onClick={() => setOpen(false)}
                    >
                        Host Meeting
                    </Link>
                </div>
            )}
        </div>
    );
}
