import logo from './logo.png';
import celebrity from './000002.jpg';
import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import RightTab from "./components/RightTab"
import './App.css';



const PersonImage = styled.img`
`
const TabWrapper = styled.div`
    margin-left: auto;
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
    display: inline-block;
    width: 500px;
    height: 100%;
`

export default function Question_vPlayer() {

    return(
    <Wrapper>
        <ImageWrapper>
            <PersonImage src={celebrity} alt="logo" />
        </ImageWrapper>
        <TabWrapper>
            <RightTab></RightTab>
        </TabWrapper>
    </Wrapper>
    );
}