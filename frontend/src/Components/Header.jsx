import {Link} from "react-router"
import { useState } from "react";
import Dropdown from "../Components/UI/Dropdown";
import { CgMenu } from "react-icons/cg";
import { CgClose } from "react-icons/cg";

export default function Header(){
    const styles = {
        links : "hover:text-[#FFDD33]"
    }

    const [isOpen, setIsOpen] = useState(false)
    const toggleIsOpen = () => {
        setIsOpen(!isOpen)
    }

    return (
        <header>
            <nav className="w-screen bg-[#0c0c0c] p-3 text-white">
                <div className="container flex justify-between items-center mx-auto">
                    <Link to="/">
                        <div className="flex items-center mx-5">
                            <img src="src/assets/Meet_Up_Logo.jpg" alt="MeetUp Logo" className="w-15 h-15"/>
                            <span className="mx-3 text-3xl font-[Silkscreen]">MeetUp</span>
                        </div>
                    </Link>
                    <div className="md:flex items-center space-x-6 font-[Silkscreen] text-xl mx-5 hidden">
                        <Dropdown/>
                        <Link to="support" className={styles.links}>
                            Support
                        </Link>
                        <Link to="signin" className={styles.links}>
                            Signin
                        </Link>
                    </div>
                    <button className="mr-10 px-2 py-2 rounded-md outline-1 cursor-pointer md:hidden" onClick={toggleIsOpen}>
                        {isOpen ? <CgClose size={25}/>: <CgMenu size={25}/>}
                    </button>
                </div>
                {isOpen && 
                    <div className="my-2 flex flex-col items-center space-y-6 font-[Silkscreen] text-xl mx-5 md:hidden">
                        <Dropdown/>
                        <Link to="support" className={styles.links}>
                            Support
                        </Link>
                        <Link to="signin" className={styles.links}>
                            Signin
                        </Link>
                    </div>
                }
            </nav>
        </header>
    );
};
