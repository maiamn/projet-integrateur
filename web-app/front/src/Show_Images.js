import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { ImageList } from '@mui/material';
import { useSelector } from 'react-redux';
import Popup from 'reactjs-popup';
import { Button} from 'react-bootstrap';
import Select from 'react-select';
import APIService from './APIService';
import { Navigate } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const PersonImage = styled.img`
    height: 130px;
    margin:3px;
    &: hover {
        cursor: pointer;
        border: 3px solid #FF0000;
    }
    border: ${props => (props.isSelected ? '3px solid #FF0000;' : '3px solid transparent')};
`
const TabWrapper = styled.div`
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
    height: 100%;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
`

const ImageGrid = styled.div`
    margin: auto;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-gap: 10px;
`

const Title = styled.h1`
  font-style: normal;
  padding-right: 100px;
  padding-left: 100px;
  font-weight: 600;
  font-size: 50px;
  line-height: 77px;
  text-align: center;
  text-transform: uppercase;
  margin-top: 20px;
  margin-bottom: 0;
`;



export default function Show_Images() {

    const [imageList, setImageList] = useState()

    const localList = JSON.parse(localStorage.getItem('selectedList'))
    console.log(localStorage.getItem('selectedList'))
    const [selectedList, setSelectedList] = useState(localList ? localList : Array(20).fill(false))

    var current_questions = JSON.parse(localStorage.getItem('currentQuestions'))  ? JSON.parse(localStorage.getItem('currentQuestions'))  : {}

    const mode = useSelector(state => state.profile.mode)

    const [to_open,setOpen]=useState(false)

    const toggleSelected=(id)=>{
        setSelectedList(() => 
            selectedList.map((image, index) => {
            if(index == id) {
                image = !image
            }
            return image;
            })
        );
    }

    const [ack_upload,setAckUpload] = useState(false)
    const [message_recu, setMessageRecu] = useState("");
    const [message_envoye, setMessageEnvoye] = useState("");
    const [reponse, setReponse] = useState("");
  
    //A CHANGER AVEC LES LOCALS STORAGE
    const id_user = 8;
    const id_partie = 9;
    const navigate = useNavigate();
    
    //fonction pour envoyer un message au dispatcher
    const sendData = (message) =>{
      APIService.sendToServer({message})
      .then(response => {
        setReponse(response); 
        setAnswer(response.answer.answer_computer); 
        localStorage.setItem('selectedList',JSON.stringify(selectedList));
        let question_here = response['question']
        current_questions[question_here] = response.answer.answer_computer;
        console.log(current_questions)
        localStorage.setItem('currentQuestions',JSON.stringify(current_questions));
        localStorage.setItem('imageList',JSON.stringify(imageList));
        navigate('/jeu_player')})
      .catch(error => console.log('error',error))
    }

    const send_answer=(e)=>{
        console.log(e)
        let message = {
            'title' : 'get_answer_computer',
            'user' : id_user,
            'id_partie' : id_partie,
            'question' : e.value
        }
        setMessageEnvoye(message)
        sendData(message)
    }

    const getImages=()=>{
        fetch('http://localhost:5000/sent',{
        credentials: "include",
        method :'POST',
        headers : {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({ 
            "message" : {
            "title": "get_n_celeb_images",
            "questions" : true,
            "user": 3,
            "id_partie": 4,
            "nb_images": 20
            }
        }),
        })
        .then(response => response.json().then(function(result){
            console.log(result.answer.images)
            let dic_images = {}
            result.answer.images.map((image, index) => {
                dic_images[index]=image
            })
            setImageList(JSON.parse(localStorage.getItem('imageList')) ? JSON.parse(localStorage.getItem('imageList')) : dic_images)
            let list = []
            console.log(result.answer.questions)
            result.answer.questions.map((i)=>{
                console.log(i)
                list = list.concat({value:i,label:i})
            })
            setOptions(list)
            setOpen(true)
        }))
        .catch(error => console.log(error))
    }

    //useEffect(() => {
      //}, [ImageList]);

    useEffect(() => {
        console.log("list",imageList)
        if (imageList===undefined && !to_open){
            getImages()
        }
    },);

    const [options,setOptions] = useState([{ value: 'No questions', label: 'No questions' }])
    const [answer,setAnswer]=useState('')
        
    console.log(selectedList)
    console.log(reponse)
    console.log(answer)
    console.log("imageList",imageList)
    return(
        <div>
    <Wrapper>
        <ImageWrapper>
            {<Title>Ask a question</Title>}
            {to_open && <Select options={options} onChange={(e)=>send_answer(e)}/>}
       
            <ImageGrid>
                {imageList && Object.entries(imageList).map(([index, image]) => {
                        return(  
                                !selectedList[index]&& 
                                    <>
                                        <PersonImage /*onClick={() => toggleSelected(index)}*/ src={`data:image/png;base64,${image}`} isSelected={selectedList[index]} alt="logo" />
                                    </>
                            )
                    
                    })
                }
            </ImageGrid>

            
        </ImageWrapper>
        
        <TabWrapper>
            <RightTab questions={current_questions} ></RightTab>
        </TabWrapper>
        
    </Wrapper>
    
    </div>
    );
}