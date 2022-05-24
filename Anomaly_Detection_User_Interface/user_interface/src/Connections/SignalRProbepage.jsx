import React, {useEffect, useState} from 'react';
import {HubConnectionBuilder, LogLevel } from '@microsoft/signalr';
import  {useLocation, useNavigate} from "react-router-dom";
import TableOfAnomalies from '../Components/TableOfAnomalies.jsx';


function SignalRProbepage(){ 
    const [Anomalydata, setAnomalyData] = useState([]);
    const [connection, setConnection] = useState(); 

    const {state} = useLocation();
    const {serialnumber} = state;
    console.log("SERIAL NUMBER");
    console.log(state);
    useEffect(() => {
        const connect = new HubConnectionBuilder()
          .withUrl("http://localhost:8081/Hub")
          .withAutomaticReconnect()
          .build();
    
        setConnection(connect);
      }, []);
    
      useEffect(() => {
        if (connection) {
          connection
            .start()
            .then(() => {
                addClientToHub();
                requestAnomalyData();
                connection.on("UpdateAnomalyTable", (response) => {
                response = JSON.parse(response);
                console.log("New data recieved");
                console.log(response);
                setAnomalyData(response);
                });
            })
            .catch((error) => console.log("Couldn't connect to hub"));
        }
      }, [connection]);

    const addClientToHub= async() => {
        try {
            await connection.invoke("AddClient", "ProbePageGroup");
        } catch (e) {
            console.log(e);
        }
    }

    const requestAnomalyData = async() => {
        try {
            await connection.invoke("SendMessage", connection.connectionId, "Probepage:GetProbeAnomalies", serialnumber)
        } catch (e) {
            console.log(e);
        }
    }
    console.log(Anomalydata)
   return (
        <div>
            <TableOfAnomalies Anomalydata={Anomalydata}/>
        </div>
    );
}
export default SignalRProbepage;