import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { useNavigate } from 'react-router-dom';
import APIService from './APIService';

const Button = styled.button`
  border: 2px solid #000000;
  width: 194px;
  height: 82px;
  font-size: 34px;
  font-weight: 700;
  margin-bottom: 20px;
  &: hover {
    cursor: pointer;
  }
`;

const PersonImage = styled.img`
    height: 130px;
    margin:3px;
    &: hover {
        cursor: pointer;
        border: 3px solid #FF0000;
    }
    opacity: ${props => (!props.stillIn ? '1' : '0.4')};
    border: ${props => (!props.stillIn ? '3px solid #FF0000;' : '3px solid transparent')};
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

    const imageList = JSON.parse(localStorage.getItem('imageList')) ? JSON.parse(localStorage.getItem('imageList')) : {}

    const current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions')) : {}

    const localList = JSON.parse(localStorage.getItem('selectedList'))
    const selectedList_last = localList ? localList : Array(20).fill(false)

    const [message_envoye, setMessageEnvoye] = useState("");
    const [reponse, setReponse] = useState("");
    const [won, setWon] = useState("")

    const id_user = localStorage.getItem('id_user')
    const id_partie = localStorage.getItem(id_user)

    const navigate = useNavigate();

    const sendData = (message) => {
        APIService.sendToServer({ message })
            .then(response => {
                setReponse(response);
                setWon(response.answer.answer_check)
            })
            .catch(error => console.log('error', error))
    }

    let last_image = ""
    console.log(last_image)
    useEffect(() => {
        if (reponse === "" && message_envoye === "" && won === "") {



            Object.entries(imageList).map(([index, image]) => {
                if (!selectedList_last[index]) {

                    last_image = JSON.parse(localStorage.getItem('imageListIds'))[index]


                }
            })

            let message = { 'title': 'check_answer', 'user': id_user, 'id_partie': id_partie, 'final_image': last_image }

            setMessageEnvoye(message)
            sendData(message)
        }
    },);

    const clear_and_go = () => {
        let user = localStorage.getItem('id_user')
        let partie = localStorage.getItem(user)

        localStorage.clear()

        localStorage.setItem('id_user', user)
        localStorage.setItem(user, partie)

        navigate('/')
    }



    return (
        <Wrapper>
            <ImageWrapper>
                {won === true && <Title>You won !</Title>}
                {won === false && <Title>You lost !</Title>}
                <ImageGrid>
                    {imageList && Object.entries(imageList).map(([index, image]) => {
                        return (
                            <>
                                <PersonImage src={`data:image/png;base64,${image}`} alt="logo" stillIn={selectedList_last[index]} />
                            </>
                        )
                    })
                    }

                </ImageGrid>
                <Button
                    type="button"
                    onClick={() => clear_and_go()}
                >Play again</Button>
            </ImageWrapper>
            <TabWrapper>
                <RightTab questions={current_questions}></RightTab>
            </TabWrapper>
        </Wrapper>
    );
}