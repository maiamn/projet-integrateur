import logo from './logo.png';
import React, { useState, useEffect } from "react";
import './App.css';
import APIService from './APIService';
import styled from 'styled-components';
import { TextField } from '@mui/material';
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux'
import { update } from './redux/profileSlice'
import { withRouter} from "react-router-dom";


const Title = styled.h1`

  width: 603px;
  height: 73px;
  
  font-style: normal;
  font-weight: 600;
  font-size: 64px;
  line-height: 77px;
  text-align: center;
  text-transform: uppercase;
`;

const PlayButton = styled.button`
  background: #D9D9D9;
  border: 2px solid #D9D9D9;
  width: 413px;
  height: 100px;
  font-size: 34px;
  &: hover {
    cursor: pointer;
    border: 2px solid #000000;
  }
`;

const EnterName = styled.p`
  margin-top: 60px;
  margin-bottom: 10px;
`

const PlayerName = styled.input`
  margin-bottom: 20px;
  background: #D9D9D9;
  width: 320px;
  height: 40px;
  font-size: 20px;
  padding-left: 5px;
`

function MainPage() {
  const navigate = useNavigate();

  const [data, setdata] = useState({
      image: ""
  });

  const dispatch = useDispatch()

  useEffect(() => {
    fetch('http://localhost:5000/db',{
      credentials: "include",
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json().then(function(result){
        setdata({image: result.data,})
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

  function test() {
    navigate("/mode");
    dispatch(update(name));
    
  }

  return (
    <div className="App">
      
      <header className="App-header">
        <Title>Guess who ?</Title>
        <img src={logo} className="App-logo" alt="logo" />
        <EnterName>Enter player's name:</EnterName>
        <PlayerName
          type="text" 
          value={name}
          onChange={(e) => handle(e.target.value)}
          //placeholder="Enter player's name"
        />
        <PlayButton type="button" onClick={()=>  { test();
       }}>
          Play
        </PlayButton>
        {/*<p>{data.message}</p>*/}
        {/* <p>{message_envoye.message}</p> */}
        {/* <TextField
          id="outlined-name"
          label="Name"
        /> */}
        
      </header>
    </div>
  );
}

export default MainPage;
