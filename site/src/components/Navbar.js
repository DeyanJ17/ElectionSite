import charts_icon from './images/election_icon.png';

const Navbar = () => {
    return (
        <nav className="py-2 border-gray-200 bg-blue-300">
            <div className="max-w-screen-xl flex justify-start mx-auto p-1">
                <div className="flex gap-3 pr-80">
                    <img src={charts_icon} alt="Charts Icon" className="h-11"></img>
                    <a className="text-3xl font-bold pr-5" href="/">Dashboard</a>
                </div>
                <div className="flex pl-40">
                    <ul className="flex flex-wrap gap-40 pt-2">
                        <li>
                            <a className="text-lg font-semibold hover:text-blue-800" href="about">About</a>
                        </li>
                        <li>
                            <a className="text-lg font-semibold hover:text-blue-800" href="map">Interactive Map</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;