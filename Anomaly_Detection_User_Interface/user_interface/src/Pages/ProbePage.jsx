import React from "react";
import Header from '../Components/Header.jsx';
import Footer from '../Components/Footer.jsx';
import SignalRProbepage from "../Connections/SignalRProbepage.jsx";
import  {useLocation, useNavigate} from "react-router-dom";


function ProbePage() {
    const text = "Anomalies Detected in CityProbe";

    // Directs the user back to the frontpage
    let navigate = useNavigate();
    const handleClick = ()=> {
        navigate('/');
    }

    return (
        <div className="probepage">  
            <button className="button" onClick={() => handleClick()}>Back to frontpage</button>
            <Header data = {text}/>
            <div className="container">
                <SignalRProbepage />
            </div>
            <Footer />
        </div>
    );
}

export default ProbePage;