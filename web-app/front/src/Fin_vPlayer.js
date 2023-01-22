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

export default function Fin_vPlayer() {

    const [imageList, setImageList] = useState(JSON.parse(localStorage.getItem('imageList'))  ? JSON.parse(localStorage.getItem('imageList'))  : {})

    
    const localList = JSON.parse(localStorage.getItem('selectedList'))
    const [selectedList, setSelectedList] = useState(localList ? localList : Array(20).fill(false))
    const [selectedList_last, setSelectedList_last] = useState(localList ? localList : Array(20).fill(false))

    const mode = useSelector(state => state.profile.mode)
    console.log('im',imageList)
    console.log('select ',selectedList_last)
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


    const [message_recu, setMessageRecu] = useState("");
    const [message_envoye, setMessageEnvoye] = useState("");
    const [reponse, setReponse] = useState("");
    const [won,setWon]=useState("")

    const sendData = (message) =>{
        APIService.sendToServer({message})
        .then(response => {setReponse(response); console.log(response); setWon(response.answer.answer_check)})
        .catch(error => console.log('error',error))
    }

    const id_user = 8;
    const id_partie = 9;
    const navigate = useNavigate();

    useEffect(() => {
        if (reponse==="" && message_envoye==="" && won===""){
            let last_image = ""
            Object.entries(imageList).map(([index, image]) => {
                if (!selectedList_last[index]){
                    last_image = image
                }
            })
            console.log(last_image)
            let message ={'title' : 'check_answer', 'user' : id_user,'id_partie' : id_partie, 'final_image' : last_image}
            setMessageEnvoye(message)
            sendData(message)
        }
    },);
        
        
    console.log(won)
    console.log(message_envoye)
    console.log(reponse)

    var current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions'))  : {}
    
    
    return(
    <Wrapper>
        <ImageWrapper>
        <Title>End of the game</Title>
        {won===true && <Title>You won !</Title> }
        {won===false && <Title>You lost !</Title> }
            <ImageGrid>
                {imageList && Object.entries(imageList).map(([index, image]) => {
                    return(  
                        !selectedList_last[index]&&
                            <>
                                <PersonImage /*onClick={() => toggleSelected(index)}*/ src={`data:image/png;base64,${image}`} isSelected={selectedList[index]} alt="logo" />
                            </>
                    )
                    })
                }
      
            </ImageGrid>
            <Button
                type="button"
                onClick={() => {
                    localStorage.clear();
                    navigate('/image')
                }}
                >Play again</Button>
        </ImageWrapper>
        <TabWrapper>
            <RightTab questions={current_questions}></RightTab>
        </TabWrapper>
    </Wrapper>
    );
}