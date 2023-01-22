import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { ImageList } from '@mui/material';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import APIService from './APIService';
import Select from 'react-select';
import Button from "./components/general/Button";
/*import { Button} from 'react-bootstrap';*/


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

export default function Question_vComputer() {

    // const localImage = JSON.parse(localStorage.getItem('selectedImage'))
    //console.log(localStorage.getItem('selectedImage'))
    // const [selectedImage, setSelectedImage] = useState(localImage ? localImage : "")
    const [image_comp,setImage]=useState('')

    var current_questions = JSON.parse(localStorage.getItem('currentQuestions'))  ? JSON.parse(localStorage.getItem('currentQuestions'))  : {}
    const [need_answer, setNeedAnswer] = useState(false)

    const [imagesLeft,setImageLeft]=useState("")
    const [question,setQuestion]=useState("")

    const mode = useSelector(state => state.profile.mode)
    
        //fonction pour envoyer un message au dispatcher
        const sendData = (message) =>{
            APIService.sendToServer({message})
            .then(response => {
              setReponse(response); 
            if (response.title==="AnswerSrV"){
                console.log('answer')
                setNeedAnswer(true);
                setImageLeft(response.answer.images_left)

                if ('question_to_ask' in response.answer){
                    setQuestion(response.answer.question_to_ask)
                }else {
                    console.log(response.answer.image)
                    setImage(response.answer.image)
                }
            }else{
                console.log('confirm')
                setNeedAnswer(false);
                setMessageEnvoye("")
                current_questions[question] = response.answer_user;
                console.log(current_questions)
                localStorage.setItem('currentQuestions',JSON.stringify(current_questions));
            }
          })
            .catch(error => console.log('error',error))
        }

        
        const [message_recu, setMessageRecu] = useState("");
        const [message_envoye, setMessageEnvoye] = useState("");
        const [reponse, setReponse] = useState("");
      
        //A CHANGER AVEC LES LOCALS STORAGE
        const id_user = 8;
        const id_partie = 9;
        const navigate = useNavigate();

        useEffect(() => {
            if (message_envoye==="" && !need_answer){
                console.log('ask')
                let message = {
                    'title' : 'get_question_to_ask',
                    'user' : id_user,
                    'id_partie' : id_partie
                }
                setMessageEnvoye(message)
                sendData(message)
            }
        },)

        const send_answer=(e)=>{
            //console.log(e)
            let message = {
                'title' : 'get_answer_user',
                'user' : id_user,
                'id_partie' : id_partie,
                'answer_user': (e.value==='Yes')
            }
            setMessageEnvoye(message)
            sendData(message)
        }
        
        console.log("need answer",need_answer)
        console.log("envoye",message_envoye)
        console.log("reponse",reponse)
        // console.log("image equals",image_comp==localImage)
        console.log("images left",imagesLeft<=1)
        console.log(imagesLeft)
        const [end,setEnd]=useState("")

    return(
    <Wrapper>
        <ImageWrapper>
            {/* {imagesLeft>1 &&<Title>Your picture</Title>} */}
            {/* {imagesLeft<=1 && image_comp===localImage &&<Title>Computer won</Title>}
            {imagesLeft<=1 && image_comp!==localImage &&<Title>Computer Lost</Title>} */}
            {image_comp && imagesLeft<=1 &&<Title>Is it the one you chose ?</Title>}
            {image_comp && imagesLeft<=1 && <Select options={[{ value: 'Yes', label: 'Yes' },{ value: 'No', label: 'No' }]} onChange={(e)=>setEnd(e.value=="Yes")}/>}
            {end===true &&<Title>Computer won</Title>}
            {end===false &&<Title>Computer Lost</Title>}
            {need_answer && imagesLeft>1 &&<Title>Question : {question}</Title>}
            {need_answer && imagesLeft>1 && <Select options={[{ value: 'Yes', label: 'Yes' },{ value: 'No', label: 'No' }]} onChange={(e)=>send_answer(e)}/>}
            <ImageGrid>
                { image_comp &&  
                        <>
                            <PersonImage src={`data:image/png;base64,${image_comp}`} alt="logo" />
                        </>
                    
                
}
            </ImageGrid>
            {imagesLeft>1 && <Title>Images left : {imagesLeft}</Title>}
            <Button
                type="button"
                onClick={() => {
                    localStorage.clear();
                    navigate('/image')
                }}
                >Play again</Button>
        </ImageWrapper>
        <TabWrapper>
            <RightTab questions={current_questions} ></RightTab>
        </TabWrapper>
    </Wrapper>
    );
}