import React, {useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';

function TableOfProbes(props){

    // Directs the user to the next page, showing all anomalies in the selected probe
    let navigate = useNavigate();
    const handleClick = (probe)=> {
        navigate('/ProbePage',{state: {
            serialnumber: probe[0], 
        }});
    }

    const MakeTable = () => {
        if(props.Probedata.length > 0){
            return(
                props.Probedata.map((entry) => (
                    <tr key={entry[0]} onClick={() => handleClick(entry)} className="pointer">
                        <td>{entry[0]}</td>
                        <td>{entry[1]}</td>
                        <td>{entry[2]}</td>
                        <td>{entry[3]}</td>
                    </tr>
                ))
            )
        }
        else {
            return(
            <tr>
                <td colSpan = {4}> No data available, please try again later !</td> 
            </tr>)
        }
    }


    // Creates the table 
    return (
        <div className="container">
            <table>
                <thead>
                <tr>
                    <th>CityProbe</th>
                    <th>Location</th>
                    <th>Latest anomaly</th> 
                    <th>No. of anomalies</th>
                </tr>
                </thead>
                <tbody>
                    {
                        MakeTable()
                    }
                </tbody>
            </table>
        </div>
    );
}
export default TableOfProbes;