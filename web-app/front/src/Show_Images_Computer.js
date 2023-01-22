import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import loader from './components/Snake.gif'

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



export default function Show_Images_Computer() {

    const localImages = JSON.parse(localStorage.getItem('imageList'))
    const [imageList, setImageList] = useState(localImages ? localImages : undefined)
    const [isLoading, setIsLoading] = useState(true)

    const localList = JSON.parse(localStorage.getItem('selectedList'))
    const selectedList = localList ? localList : Array(20).fill(false)

    const current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions')) : {}

    const id_user = localStorage.getItem('id_user')
    const id_partie = localStorage.getItem(id_user)

    const navigate = useNavigate();

    const getImages = (message) => {
        setIsLoading(true)
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
                    setIsLoading(false)
                }
            }))
            .catch(error => console.log(error))
    }

    useEffect(() => {
        if (imageList === undefined) {
            if (imageList === undefined) {
                let message = {
                    "message": {
                        "title": "get_images",
                        "mode_image": localStorage.getItem('mode_image'),
                        "questions": false,
                        "user": id_user,
                        "id_partie": id_partie,
                        "nb_images": 20
                    }
                }
                getImages(message)
            }

        }
    },);


    return (
        <Wrapper>
            <ImageWrapper>
                {<Title>Choose an image</Title>}
                {isLoading && <img src={loader} alt="loading..." />}
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

                <Button type="button" onClick={() => navigate('/question_computer')}>Done</Button>
            </ImageWrapper>

            <TabWrapper>
                <RightTab questions={current_questions} ></RightTab>
            </TabWrapper>

        </Wrapper>


    );
}