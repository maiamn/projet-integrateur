import React, { useState } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { useNavigate } from 'react-router-dom';
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

export default function Jeu_vPlayer() {

    const imageList = JSON.parse(localStorage.getItem('imageList')) ? JSON.parse(localStorage.getItem('imageList')) : undefined;

    const navigate = useNavigate();

    const localList = JSON.parse(localStorage.getItem('selectedList'))
    const [selectedList, setSelectedList] = useState(localList ? localList : Array(20).fill(false))
    const selectedList_last = localList ? localList : Array(20).fill(false)

    const current_questions = JSON.parse(localStorage.getItem('currentQuestions')) ? JSON.parse(localStorage.getItem('currentQuestions')) : {}

    const toggleSelected = (id) => {
        setSelectedList(() =>
            selectedList.map((image, index) => {
                if (index == id) {
                    image = !image
                }
                return image;
            })
        );
    }

    const send_answer = () => {
        localStorage.setItem('selectedList', JSON.stringify(selectedList));

        let one_left = 0

        selectedList.map((i) => {
            console.log(i)
            if (i === false) {
                one_left = one_left + 1
            }
        })

        if (one_left <= 1) {
            navigate("/fin_player");
        } else {
            navigate("/show_images");
        }
    }

    return (
        <Wrapper>
            <ImageWrapper>
                <Title>Click on the picture you want to delete</Title>
                <ImageGrid>
                    {imageList && Object.entries(imageList).map(([index, image]) => {
                        return (
                            !selectedList_last[index] &&
                            <>
                                <PersonImage onClick={() => toggleSelected(index)} src={`data:image/png;base64,${image}`} isSelected={selectedList[index]} alt="logo" />
                            </>
                        )
                    })
                    }
                </ImageGrid>
                <Button
                    type="button"
                    onClick={() => send_answer()}
                >DELETE</Button>
            </ImageWrapper>
            <TabWrapper>
                <RightTab questions={current_questions}></RightTab>
            </TabWrapper>
        </Wrapper>
    );
}