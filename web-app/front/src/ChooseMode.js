import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux';
import Button from "./components/general/Button";

const Title = styled.h1`
  font-style: normal;
  padding-right: 100px;
  padding-left: 100px;
  font-weight: 600;
  font-size: 64px;
  line-height: 77px;
  text-align: center;
  text-transform: uppercase;
`;

const Paragraph = styled.p`
  text-align: center;
  font-weight: 100;
  font-size: 24px;
  line-height: 29px;
`;

const List = styled.ul`
  max-width: 346px;
  font-weight: 400;
  font-size: 17px;
  line-height: 21px;
`;

const General = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

export default function ChooseMode() {
  const dispatch = useDispatch()
  const navigate = useNavigate();

  function setMode(mode) {
    if (mode===0){
      localStorage.setItem("mode", "0")
      navigate("/show_images");
    }else{
      localStorage.setItem("mode", "1")
      navigate("/question_computer");
    }
  }

  return (
    <>
      <General>
        <Title>Choose the mode</Title>
        <Button type="button" onClick={()=> setMode(0)}>Try to guess</Button>
        <Button type="button" onClick={()=> setMode(1)}>Computer tries to guess</Button>
        <Paragraph>Precisions on the different modes :</Paragraph>
        <List>
          <li>
            Try to guess : The computer chooses a picture and answers to your
            questions. Your are the one guessing.
          </li>
          <li>
            Computer tries to guess : You choose a picture and answer to the
            question. The computer tries to guess.
          </li>
        </List>
      </General>
    </>
  );
}
