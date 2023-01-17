import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { useNavigate } from "react-router-dom";
import APIService from "./APIService";



const PersonImage = styled.img`
`
const TabWrapper = styled.div`
    margin-left: auto;
    display: inline-block;
    width: 349px;
    height: 100%;
`
const Wrapper = styled.div`
    flex-direction: row;
    display: flex;
    height: 100vh;
`

const ImageWrapper = styled.div`
    display: inline-block;
    width: 500px;
    height: 100%;
`

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
  
export default function Question_vPlayer() {

      //fonction pour récuperer des datas
  const getData= () => {
    fetch('http://localhost:5000/get_question_to_ask',{
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
    if (message_envoye!=="" && message_envoye['title']==='get_question_to_ask' && reponse['title']==="ConfirmSrv" && reponse['user']===message_envoye['user'] && reponse['id_partie']===message_envoye['id_partie'] && (message_recu['title']!=="AnswerSrv" ||message_recu['confirm']!==true || message_recu['id_partie']!==message_envoye['id_partie'] ||message_recu['user']!==message_envoye['user'])){
      console.log("Get data again")
      getData()
    }

  });


    const [message_recu, setMessageRecu] = useState("");
    const [message_envoye, setMessageEnvoye] = useState("");
    const [reponse, setReponse] = useState("");

    const id_user = 8;
    const id_partie = 9;

    //fonction pour envoyer un message au dispatcher
    const sendData = (message) =>{
        APIService.sendToServer({message})
        .then(response => setReponse(response))
        .catch(error => console.log('error',error))
    }

    const get_question_to_ask = () =>{
        console.log("function get question to ask")
    
        //message à envoyer
        let mess = { 'title' : 'get_question_to_ask', 'user' : id_user, 'id_partie' : id_partie}
        setMessageEnvoye(mess)
        sendData(mess)
    }

    return(
    <Wrapper>
        <ImageWrapper>
            <PersonImage src={celebrity} alt="logo" />
        </ImageWrapper>
        <TabWrapper>
            <RightTab></RightTab>
        </TabWrapper>

        <Button
          type="button"
          onClick={get_question_to_ask}
        >
          Test get question
        </Button>
    </Wrapper>
    );
}