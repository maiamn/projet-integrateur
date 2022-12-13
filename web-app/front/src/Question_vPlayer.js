import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { ImageList } from '@mui/material';

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

export default function Question_vPlayer() {
    const[gameState, setGameState] = useState("delete picture")

    const [imageList, setImageList] = useState([
        {id : 1, img : celebrity, isSelected : false}, {id : 2, img : celebrity, isSelected : false}, 
        {id : 3, img : celebrity, isSelected : false}])

        /*{img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false},
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}, 
        {img : celebrity, isSelected : false}, {img : celebrity, isSelected : false}*/

    const toggleSelected=(id)=>{
        setImageList(() =>
            imageList.map((image) => {
            if (image.id == id) {
                image.isSelected = !image.isSelected
            }

            return image;
            })
        );
    }

    useEffect(() => {
      }, [ImageList]);
        
    console.log(imageList)
    return(
    <Wrapper>
        <ImageWrapper>
            {gameState == "delete picture" ? <Title>select the pictures to delete</Title> : <></>}
            <ImageGrid>
                {imageList.map((image) => {
                    return(  
                        <>
                            <PersonImage onClick={() => toggleSelected(2)} src={image.img} isSelected={image.isSelected} alt="logo" />
                        </>
                    )
                    })
                }
            </ImageGrid>
        </ImageWrapper>
        <TabWrapper>
            <RightTab></RightTab>
        </TabWrapper>
    </Wrapper>
    );
}