import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import ImportImages from "./components/Upload/ImportImages";
import loader from './components/Snake.gif'
import { useState } from "react";



const Button = styled.button`
  background: #d9d9d9;
  border: 2px solid #d9d9d9;
  text-align: center;
  margin: 10px;
  width: 413px;
  height: 100px;
  font-size: 34px;
  &: hover {
    cursor: pointer;
    border: 2px solid #000000;
  }
`;

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

const General = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;


export default function ChooseImage() {

  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false)

  return (
    <>
      <General>
        {isLoading ? <img style={{ 'marginTop': '300px' }} src={loader} alt="loading..." /> :
          <>
            <Title>What pictures do you want to play with ?</Title>
            <Button
              type="button"
              onClick={() => {
                localStorage.setItem('mode_image', 'random')
                navigate("/mode");
              }}
            >
              Random
            </Button>
            <ImportImages setIsLoading={setIsLoading}></ImportImages>
          </>}
      </General>
    </>
  );
}
