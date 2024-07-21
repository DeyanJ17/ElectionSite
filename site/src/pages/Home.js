import electionData from './imports/data.json';
import prediction from './imports/JulyPrediction.png';
import simulation from './imports/simulation.json';

function getLink(state) {
    if (state.includes(" ")) {
        const stateIndex = state.split(" ");
        state = stateIndex[0] + "-" + stateIndex[1];
    }
    return "https://projects.fivethirtyeight.com/polls/president-general/2024/" + state.toLowerCase()
}

const Home = () => {
    let swing = []
    let leanD = []
    let leanR = []

    const lead_value = electionData["National"][1]
    let lead_style = "font-bold flex justify-center pt-1 text-xl ";
    if (lead_value.charAt(0) == "D") {
        lead_style += "text-blue-800";
    } else {
        lead_style += "text-red-800";
    }

    for (let state in electionData) {
        let state_lead = electionData[state][1]
        if (state == "National" || electionData[state] == "No Polls") {
            continue;
        }
        else if (parseFloat(state_lead.substring(3)) <= 2.5) {
            swing.push(state);
        }
        else if (state_lead.charAt(0) == "D") {
            if (parseFloat(state_lead.substring(3)) <= 6) {
                leanD.push(state);
            }
        }
        else if (state_lead.charAt(0) == "R") {
            if (parseFloat(state_lead.substring(3)) <= 6) {
                leanR.push(state);
            }
        }
    }

    return (
        <body className="bg-gray-300">
            <div className="flex flex-wrap">
                <aside id="default-sidebar" class="top-50 left-0 z-80 w-60 h-screen-full bg-gray-500" aria-label="Sidebar">
                    <h1 className="flex justify-center font-bold bg-emerald-500 text-3xl pt-2 pb-2">Ratings</h1>
                    <div className="pt-2 pb-2 bg-stone-50">
                        <h2 className="font-semibold text-xl pl-2">Swing States</h2>
                        {swing.map((state) =>
                            {
                                let hoverClass = "pl-4 hover:shadow-xl hover:bg-gray-200"
                                const link = getLink(state);
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href={link}>• {state}</a>
                                    </div>
                                );
                            }
                        )}
                    </div>
                    <div className="pt-2 pb-2 bg-blue-200">
                        <h2 className="font-semibold text-xl pl-2">Lean Harris States</h2>
                        {leanD.map((state) =>
                            {
                                let hoverClass = "pl-4 hover:shadow-xl hover:bg-blue-400"
                                const link = getLink(state);
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href={link}>• {state}</a>
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
                                const link = getLink(state);
                                return (
                                    <div key={state} className={hoverClass}>
                                        <a href={link}>• {state}</a>
                                    </div>
                                );
                            }
                        )}
                    </div>
                </aside>

                <div>
                    <div className="flex justify-center pl-60 pt-10">
                        <div className="flex flex-col px-6 py-5 border-2 border-black bg-emerald-300">
                            <h1 className="font-bold text-2xl flex justify-center">National Average</h1>
                            <div className="flex flex-wrap justify-center pt-2">
                                <h1 className="font-semibold text-blue-600">Harris (D)</h1>: {electionData["National"][0]["Harris"]}%
                            </div>
                            <div className="flex flex-wrap justify-center">
                                <h1 className="font-semibold text-red-600">Trump (R)</h1>: {electionData["National"][0]["Trump"]}%
                            </div>
                            <div className="flex flex-wrap justify-center">
                                <h1 className="font-semibold text-gray-600">Others</h1>: {(100-(electionData["National"][0]["Harris"]+electionData["National"][0]["Trump"])).toFixed(2)}%
                            </div>
                            <div className={lead_style}>
                                {electionData["National"][1]}
                            </div>
                            <div className="pt-3">
                                <h1 className="font-bold text-2xl flex justify-center">Model Odds</h1>
                                <div className="flex justify-center">
                                    <h1 className="font-semibold text-blue-600">Harris</h1>: {simulation[0]} in 100
                                    <h1 className="font-semibold text-red-600 pl-4">Trump</h1>: {simulation[1]} in 100
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="pl-60 pt-5">
                        <h1 className="flex justify-center text-4xl pb-3 font-bold">My Prediction</h1>
                        <div className="flex flex-wrap">
                            <a href="#"></a>
                            <img src={prediction} width="850"></img>
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