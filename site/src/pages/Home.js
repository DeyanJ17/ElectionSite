import electionData from './imports/data.json'

const Home = () => {
    const swing = ["Arizona", "Pennsylvania", "Wisconsin"]
    const leanD = ["Maine: At Large", "Minnesota", "Michigan", "Nebraska: District 1", "New Hampshire", "New Mexico", "Virginia"]
    const leanR = ["Florida", "Georgia", "Nevada", "North Carolina", "Ohio", "Texas"]

    const lead_value = electionData["National"][1]
    let lead_style = "font-bold flex justify-center pt-1 text-xl ";
    if (lead_value.charAt(0) == "D") {
        lead_style += "text-blue-800";
    } else {
        lead_style += "text-red-800";
    }

    return (
        <body className="bg-gray-300">
            <div className="flex flex-wrap">
                <aside id="default-sidebar" class="top-50 left-0 z-80 w-60 h-screen-full bg-gray-500" aria-label="Sidebar">
                    <h1 className="flex justify-center font-bold bg-emerald-500 text-3xl pt-2 pb-2">Ratings Sidebar</h1>
                    <div className="pt-2 pb-2 bg-stone-50">
                        <h2 className="font-semibold text-xl pl-2">Swing States</h2>
                        {swing.map((state) =>
                            {
                                let hoverClass = "pl-4 hover:shadow-xl hover:bg-gray-200"
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href="#">• {state}</a>
                                    </div>
                                );
                            }
                        )}
                    </div>
                    <div className="pt-2 pb-2 bg-blue-200">
                        <h2 className="font-semibold text-xl pl-2">Lean Biden States</h2>
                        {leanD.map((state) =>
                            {
                                let hoverClass = "pl-4 hover:shadow-xl hover:bg-blue-400"
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href="#">• {state}</a>
                                    </div>
                                );
                            }
                        )}
                    </div>
                    <div className="pt-2 pb-2 bg-red-200">
                        <h2 className="font-semibold text-xl pl-2">Lean Trump States</h2>
                        {leanR.map((state) =>
                            {
                                let hoverClass = "pl-4 hover:shadow-xl hover:bg-red-400"
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href="#">• {state}</a>
                                    </div>
                                );
                            }
                        )}
                    </div>
                </aside>

                <div>
                    <div className="flex justify-center pl-60 pt-10">
                        <div className="flex flex-col px-6 py-5 border-2 border-black bg-emerald-300">
                            <h1 className="font-bold text-2xl">National Average</h1>
                            <div className="flex flex-wrap justify-center pt-2">
                                <h1 className="font-semibold text-blue-600">Biden (D)</h1>: {electionData["National"][0]["Biden"]}%
                            </div>
                            <div className="flex flex-wrap justify-center">
                                <h1 className="font-semibold text-red-600">Trump (R)</h1>: {electionData["National"][0]["Trump"]}%
                            </div>
                            <div className="flex flex-wrap justify-center">
                                <h1 className="font-semibold text-gray-600">Others</h1>: {(100-(electionData["National"][0]["Biden"]+electionData["National"][0]["Trump"])).toFixed(2)}%
                            </div>
                            <div className={lead_style}>
                                {electionData["National"][1]}
                            </div>
                        </div>
                    </div>
                    <div className="pl-60 pt-5">
                        <h1 className="flex justify-center text-4xl pb-3 font-bold">My Prediction</h1>
                        <div className="flex flex-wrap">
                            <a href="https://www.270towin.com/maps/NDlOA"></a>
                            <img src="https://www.270towin.com/map-images/NDlOA.png" width="800"></img>
                        </div>
                        <div className="flex justify-center pt-5 pb-2">
                            <p>For more detailed insight (and an explanation for my predictions), visit the 
                                <a href="blogdisplay" className="text-blue-600 text-underline"> blogs</a> tab.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        
    );
}

export default Home;