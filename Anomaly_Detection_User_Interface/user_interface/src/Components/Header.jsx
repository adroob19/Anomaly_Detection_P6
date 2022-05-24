import React from "react";
import logo from '../logo.png';

function Header(props) {
    return (
        <header className="App-header">
            <img className="App-logo" src={logo} alt="Logo" />
            <h1>{props.data}</h1>
        </header>  
    )
}

export default Header;