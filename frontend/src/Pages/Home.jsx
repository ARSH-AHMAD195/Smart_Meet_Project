import { Link } from "react-router"

function Home() {
  return (
    <div className="w-screen min-h-[calc(100vh-84px)] py-20 bg-linear-0 from-[#2b2b2b] to-[#0c0c0c]">
        <div className="mx-30  flex flex-col space-y-6 items-center md:py-10">
            <div>
                <h1 className="text-center text-white text-6xl font-[Poppins] font-extrabold md:text-9xl">YOUR MEETINGS</h1>
                <h1 className="text-center text-[#FFDD22] text-6xl font-[Poppins] font-extrabold md:text-9xl">UPGRADED</h1>
            </div>``
            <p className="text-center text-white text-[12px] font-[Poppins] md:px-20 md:text-xl">
                Work smarter with seamless communication powered by integrated AI. Whether you're teaming up on ideas or supporting customers, everything becomes faster, clearer, and more productive.
            </p>
            
            <button className="w-50 h-12 bg-white rounded-md text-xl font-[Silkscreen] cursor-pointer md:w-1/4">
                <Link to={"/myhome"}>Schedule meet</Link>
            </button>
        </div>
    </div>
  )
}

export default Home