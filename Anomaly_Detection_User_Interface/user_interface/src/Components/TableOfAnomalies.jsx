import React from "react";

function TableOfAnomalies(props) {

    const MakeTable = () => {
        if(props.Anomalydata.length > 0){
            return(
                props.Anomalydata[4].map((entry) => (
                    <tr key={entry[0]} className="noHover">
                        <td>{entry[0]}</td>
                        <td>{entry[1]}</td>
                        <td>{entry[2]}</td>
                        <td>{entry[3]}</td>
                        <td>{entry[4]}</td>
                        <td>{entry[5]}</td>
                        <td>{entry[6]}</td>
                        <td>{entry[7]}</td>
                    </tr>
                ))
            )
        }
        else {
            return(
            <tr>
                <td colSpan = {8}> No data available, please try again later !</td> 
            </tr>)
        }
    }

    const MakeProbeInfo = ()=>{
        if(props.Anomalydata.length > 0){
            return(
                <>
                    <h4> 
                    <b>CityProbe:</b> {props.Anomalydata[0]} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                    <b>Location:</b> {props.Anomalydata[1]} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                    <b>Latitude:</b> {props.Anomalydata[2]} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                    <b>Longitude:</b> {props.Anomalydata[3]} 
                    </h4>
                </>
            )  
        }
        else{
            return(
                <>
                <h4> 
                <b>CityProbe:</b> error &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                <b>Location:</b> error &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                <b>Latitude:</b> error &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                <b>Longitude:</b> error 
                </h4>
            </>
            )
        }
    }

    return (
        <div className="containerAnomalies">
            {
                MakeProbeInfo()
            } 
            <table>
                <thead>
                <tr className="noHover">
                    <th>Time of anomaly</th>
                    <th>Luminosity</th>
                    <th>Temperature</th>
                    <th>Humidity</th>
                    <th>PM10</th>
                    <th>PM25</th>
                    <th>NO2</th>
                    <th>CO</th>
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

export default TableOfAnomalies;