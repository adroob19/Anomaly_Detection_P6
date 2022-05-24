// https://app.pluralsight.com/guides/dynamic-tables-from-editable-columns-in-react-html
import React, {useEffect, useState} from 'react';
import {HubConnectionBuilder, LogLevel } from '@microsoft/signalr';
import TableOfProbes from '../Components/TableOfProbes.jsx';


function SignalRFrontpage(){
    // Creates a state variable/array with the data
    const [Probedata, setProbeData] = useState([]);
    const [connection, setConnection] = useState(); 
    

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
                requestProbeData();
                connection.on("UpdateProbeTable", (response) => {
                response = JSON.parse(response);
                console.log("New data recieved");
                console.log(response);
                setProbeData(response);
                });
            })
            .catch((error) => console.log("Couldn't connect to hub"));
        }
      }, [connection]);

    const addClientToHub= async() => {
        try {
            await connection.invoke("AddClient", "FrontPageGroup");
        } catch (e) {
            console.log(e);
        }
    }

    const requestProbeData = async() => {
        try {
            await connection.invoke("SendMessage", connection.connectionId, "Frontpage:GetProbeInformation", "")
        } catch (e) {
            console.log(e);
        }
    }

   return (
        <div>
            <TableOfProbes Probedata={Probedata}/>
        </div>
    );
}
export default SignalRFrontpage;