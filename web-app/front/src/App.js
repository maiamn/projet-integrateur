import logo from './logo.png';
import React, { useState, useEffect } from "react";
import './App.css';
import APIService from './APIService';

function App() {

  const [data, setdata] = useState({
      message: "rien"
  });



  useEffect(() => {
    fetch('http://localhost:5000/',{
      credentials: "include",
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json().then(function(result){
        console.log(result)
        setdata({message: result.message,})
      }))
    .catch(error => console.log(error))
    
  }, []);

  const [message_recu, setMessageRecu] = useState("");
  const [message_envoye, setMessageEnvoye] = useState({message:""});

  const sendData = (message) =>{
    APIService.sendToServer({message})
    .then(response => setMessageEnvoye(response))
    .catch(error => console.log('error',error))
  }

  const [name,setName] = useState("");

  const handle=(e)=>{
    setName(e)
  }

  console.log(message_envoye)

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Who am I ? Play now.
        </p>
        <input
          type="text" 
          value={name}
          onChange={(e) => handle(e.target.value)}
          placeholder='Enter player'
        />
        <button type="button" onClick={()=> sendData({'name':name})}>SUBMIT</button>
        {/*<p>{data.message}</p>*/}
        <p>{message_envoye.message}</p>
        
      </header>
    </div>
  );
}

export default App;
