import React from 'react';
import Header from '../Components/Header.jsx';
import Footer from '../Components/Footer.jsx';
import SignalRFrontpage from "../Connections/SignalRFrontpage.jsx";

function Frontpage() {
  const text = "Anomaly Detection in CityProbe data"
  return (
    <div className="frontpage">
      <Header data = {text}/>
      <div className="container">
        <SignalRFrontpage/>
      </div>
      <Footer />
    </div>
  );
}

export default Frontpage;















