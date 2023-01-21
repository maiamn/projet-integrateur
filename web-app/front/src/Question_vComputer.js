import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { useNavigate } from 'react-router-dom';
import APIService from './APIService';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

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

    const [image_comp, setImage] = useState('')

    const current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions')) : {}

    const [need_answer, setNeedAnswer] = useState(false)

    const [imagesLeft, setImageLeft] = useState("")

    const [question, setQuestion] = useState("")

    const [end, setEnd] = useState("")

    const [message_envoye, setMessageEnvoye] = useState("");

    const id_user = localStorage.getItem('id_user')
    const id_partie = localStorage.getItem(id_user)

    const navigate = useNavigate();


    const sendData = (message) => {
        APIService.sendToServer({ message })
            .then(response => {


                if (response.title === "AnswerSrV") {

                    setNeedAnswer(true);
                    setImageLeft(response.answer.images_left)

                    if ('question_to_ask' in response.answer) {
                        setQuestion(response.answer.question_to_ask)
                    } else {
                        if ('image' in response.answer) {
                            setImage(response.answer.image)
                        } else {
                            setEnd(false)
                        }
                    }

                } else {

                    setNeedAnswer(false);
                    setMessageEnvoye("")
                    current_questions[question] = response.answer_user;
                    localStorage.setItem('currentQuestions', JSON.stringify(current_questions));

                }
            })
            .catch(error => console.log('error', error))
    }


    useEffect(() => {
        if (message_envoye === "" && !need_answer) {
            let message = {
                'title': 'get_question_to_ask',
                'user': id_user,
                'id_partie': id_partie,
                'excluded': current_questions
            }
            setMessageEnvoye(message)
            sendData(message)
        }
    },)

    const send_answer = (e) => {
        let message = {
            'title': 'get_answer_user',
            'user': id_user,
            'id_partie': id_partie,
            'answer_user': (e.value === 'Yes'),
            'question': question
        }
        setMessageEnvoye(message)
        sendData(message)
    }

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

                {image_comp && imagesLeft == 1 && <Title>Is it the one you chose ?</Title>}
                {image_comp && imagesLeft == 1 && <Select options={[{ value: 'Yes', label: 'Yes' }, { value: 'No', label: 'No' }]} onChange={(e) => setEnd(e.value == "Yes")} />}

                {end === true && <Title>Computer won</Title>}
                {end === false && <Title>Computer Lost</Title>}
                {imagesLeft == 0 && <Title>No picture corresponds</Title>}

                {need_answer && imagesLeft > 1 && <Title>Question : {question}</Title>}
                {need_answer && imagesLeft > 1 && <Select options={[{ value: 'Yes', label: 'Yes' }, { value: 'No', label: 'No' }]} onChange={(e) => send_answer(e)} />}
                {image_comp && imagesLeft == 1 &&
                    <ImageGrid>
                        <>
                            <PersonImage src={`data:image/png;base64,${image_comp}`} alt="logo" />
                        </>

                    </ImageGrid>}

                {imagesLeft > 1 && <Title>Images left : {imagesLeft}</Title>}

                {imagesLeft <= 1 && end !== "" &&
                    <Button
                        type="button"
                        onClick={() => clear_and_go()}
                    >Play again</Button>
                }

            </ImageWrapper>

            <TabWrapper>
                <RightTab questions={current_questions} ></RightTab>
            </TabWrapper>
        </Wrapper>
    );
}