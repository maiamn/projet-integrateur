import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import APIService from "./APIService";
import { getAccordionDetailsUtilityClass } from "@mui/material";


const Button = styled.button`
  background: #d9d9d9;
  border: 2px solid #d9d9d9;
  text-align: center;
  margin: 10px;
  width: 413px;
  height: 100px;
  font-size: 34px;
  &: hover {
    cursor: pointer;
    border: 2px solid #000000;
  }
`;

const Title = styled.h1`
  font-style: normal;
  padding-right: 100px;
  padding-left: 100px;
  font-weight: 600;
  font-size: 64px;
  line-height: 77px;
  text-align: center;
  text-transform: uppercase;
`;

const General = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;


export default function ChooseImage() {
  const getData= () => {
    fetch('http://localhost:5000/return',{
      credentials: "include",
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json().then(function(result){
      console.log(result)
      setMessageRecu(result)
      }))
    .catch(error => console.log(error))
  }

  useEffect(() => {
    
    if (message_envoye!=="" && message_envoye['title']==='upload' && reponse['title']==="ConfirmSrv" && (message_recu['title']!=="AnswerSrv" ||message_recu['confirm']!==true)){
      console.log("get data")
      console.log("envoye",message_envoye)
      console.log("recu",message_recu)
      getData()
    }
    
  });
  
  const [message_recu, setMessageRecu] = useState("");
  const [message_envoye, setMessageEnvoye] = useState("");
  const [reponse, setMessageReponse] = useState("");
  
  const sendData = (message) =>{
    APIService.sendToServer({message})
    .then(response => setMessageReponse(response))
    .catch(error => console.log('error',error))
  }

  const send_images = () =>{
    console.log("send images")
    let mess = {'title':'upload'}
    setMessageEnvoye(mess)
    sendData(mess)
  }

  const navigate = useNavigate();

  console.log("mess recu",message_recu)
  console.log("mess env",message_envoye)
  console.log("mess rep",reponse)

  return (
    <>
      <General>
        <Title>What pictures do you want to play with ?</Title>
        <Button
          type="button"
          onClick={() => {
            navigate("/mode");
          }}
        >
          Random
        </Button>
        <Button
          type="button"
          onClick={send_images}
        >
          Upload from computer
        </Button>
      </General>
    </>
  );
}
