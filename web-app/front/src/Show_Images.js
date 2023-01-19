import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import Select from 'react-select';
import APIService from './APIService';
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

    const localImages = JSON.parse(localStorage.getItem('imageList'))
    const [imageList, setImageList] = useState(localImages ? localImages : undefined)

    const localList = JSON.parse(localStorage.getItem('selectedList'))
    const selectedList = localList ? localList : Array(20).fill(false)

    const current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions')) : {}


    const options_questions = JSON.parse(localStorage.getItem('options_question'))
    const [options, setOptions] = useState(options_questions ? options_questions : [{ value: 'No questions', label: 'No questions' }])
    const [optionOk, setOk] = useState(options_questions ? true : false)

    const [to_open, setOpen] = useState(options_questions ? true : false)

    const id_user = localStorage.getItem('id_user')
    const id_partie = localStorage.getItem(id_user)

    const navigate = useNavigate();


    //fonction pour envoyer un message au dispatcher
    const sendData = (message) => {
        APIService.sendToServer({ message })
            .then(response => {

                localStorage.setItem('selectedList', JSON.stringify(selectedList));

                let question_here = response['question']
                current_questions[question_here] = response.answer.answer_computer;
                localStorage.setItem('currentQuestions', JSON.stringify(current_questions));

                navigate('/jeu_player')
            })

            .catch(error => console.log('error', error))
    }

    const send_answer = (e) => {
        let message = {
            'title': 'get_answer_computer',
            'user': id_user,
            'id_partie': id_partie,
            'question': e.value
        }

        sendData(message)
    }

    const getImages = (message) => {
        fetch('http://localhost:5000/sent', {
            credentials: "include",
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(message),
        })
            .then(response => response.json().then(function (result) {
                if ("images" in result.answer) {
                    console.log("images", result.answer.images)
                    let dic_images = {}
                    result.answer.images.map((image, index) => {
                        dic_images[index] = image
                    })
                    setImageList(dic_images)
                    localStorage.setItem('imageList', JSON.stringify(dic_images));
                }

                let list = []
                console.log("questions", result.answer.questions)
                Object.entries(result.answer.questions).map(([index, question]) => {
                    list = list.concat({ value: index, label: question })
                })
                localStorage.setItem('options_question', JSON.stringify(list))
                setOptions(list)
                setOk(true)
                setOpen(true)
            }))
            .catch(error => console.log(error))
    }

    useEffect(() => {
        if ((imageList === undefined || !optionOk) && !to_open) {
            if (imageList === undefined) {
                let message = {
                    "message": {
                        "title": "get_images",
                        "questions": true,
                        "user": id_user,
                        "id_partie": id_partie,
                        "nb_images": 20
                    }
                }
                getImages(message)
            } else {
                let message = {
                    "message": {
                        "title": "get_questions",
                        "user": id_user,
                        "id_partie": id_partie
                    }
                }
                getImages(message)
            }

        }
    },);


    return (
        <Wrapper>
            <ImageWrapper>
                {<Title>Ask a question</Title>}
                {to_open && <Select options={options} onChange={(e) => send_answer(e)} />}

                <ImageGrid>
                    {imageList && Object.entries(imageList).map(([index, image]) => {
                        return (
                            !selectedList[index] &&
                            <>
                                <PersonImage src={`data:image/png;base64,${image}`} /*isSelected={selectedList[index]}*/ alt="logo" />
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


    );
}