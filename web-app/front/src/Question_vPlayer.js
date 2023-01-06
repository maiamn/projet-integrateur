import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';
import { ImageList } from '@mui/material';
import { useSelector } from 'react-redux';

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

    const [imageList, setImageList] = useState()

    const [selectedList, setSelectedList] = useState(Array(20).fill(false))

    const mode = useSelector(state => state.profile.mode)

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

    useEffect(() => {
      }, [ImageList]);

    useEffect(() => {
        fetch('http://localhost:5000/celebs',{
        credentials: "include",
        method :'POST',
        headers : {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({ 
            "title": "get_n_celeb_images",
            "user": 3,
            "id_partie": 4,
            "nb_images": 20
        })
        })
        .then(response => response.json().then(function(result){
            console.log(result.answer.images)
            setImageList(result.answer.images)
        }))
        .catch(error => console.log(error))
        
    }, []);
    
        
    console.log(selectedList)
    return(
    <Wrapper>
        <ImageWrapper>
            {mode == 0 ? <Title>select the pictures to delete</Title> : <Title>select the picture to guess</Title>}
            <ImageGrid>
                {imageList && imageList.map((image, index) => {
                    return(  
                        <>
                            <PersonImage onClick={() => toggleSelected(index)} src={`data:image/png;base64,${image}`} isSelected={selectedList[index]} alt="logo" />
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