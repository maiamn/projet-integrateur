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

  //fonction pour récuperer des datas
  const getData= () => {
    fetch('http://localhost:5000/get_labels',{
      credentials: "include",
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json().then(function(result){

      //on récupère le message reçu
      setMessageRecu(result)

      }))
    .catch(error => console.log(error))
  }

  //useEffect continue de se ré-executer tant que l'on ne l'arrête pas (ici jamais mais ne fait rien si les conditions des ifs ne sont pas remplies)
  useEffect(() => {
    
    //si on a bien envoyé un message, que ce message est bien celui où on upload les images et que l'on a reçu la confirmation que le gestCNN a bien reçu les images, tant que l'on a pas reçu le bon message on demande
    if (message_envoye!=="" && message_envoye['title']==='get_labels' && reponse['title']==="ConfirmSrv" && reponse['user']===message_envoye['user'] && reponse['id_partie']===message_envoye['id_partie'] && (message_recu['title']!=="AnswerSrv" ||message_recu['confirm']!==true || message_recu['id_partie']!==message_envoye['id_partie'] ||message_recu['user']!==message_envoye['user'])){
      console.log("Get data again")
      getData()
    }
    
  });
  
  const [message_recu, setMessageRecu] = useState("");
  const [message_envoye, setMessageEnvoye] = useState("");
  const [reponse, setReponse] = useState("");

  //A CHANGER AVEC LES LOCALS STORAGE
  const id_user = 8;
  const id_partie = 9;
  
  //fonction pour envoyer un message au dispatcher
  const sendData = (message) =>{
    APIService.sendToServer({message})
    .then(response => setReponse(response))
    .catch(error => console.log('error',error))
  }

  const send_images = () =>{
    console.log("function send images")

    //message à envoyer
    let mess = { 'title' : 'get_labels', 'user' : id_user, 'id_partie' : id_partie}
    setMessageEnvoye(mess)
    sendData(mess)
  }

  const navigate = useNavigate();

  console.log("mess recu",message_recu)
  console.log("mess env",message_envoye)
  console.log("reponse",reponse)

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
