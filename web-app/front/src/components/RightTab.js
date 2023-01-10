import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import { useSelector } from 'react-redux';
import { useNavigate } from "react-router-dom";


const Tab = styled.div`
  width: 100%;
  height: 100%;
  background: #D9D9D9;
  font-size: 34px;
  text-align: center;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
`;

const Wrapper = styled.div`
  display: flex;
  position: relative;
  height: inherit;
  width: inherit;
`;

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

const Buttons = styled.div`
  margin-top: auto;
`;



export default function RightTab() {

  const [isActive, setIsActive] = useState(true);
  const [isPaused, setIsPaused] = useState(false);
  const [time, setTime] = useState(0);
  const name = useSelector(state => state.profile.value)
  const navigate = useNavigate();



  React.useEffect(() => {
    let interval = null;
  
    if (isActive && isPaused === false) {
      interval = setInterval(() => {
        setTime((time) => time + 10);
      }, 10);
    } else {
      clearInterval(interval);
    }
    return () => {
      clearInterval(interval);
    };
  }, [isActive, isPaused]);
  
  const handleStart = () => {
    setIsActive(true);
    setIsPaused(false);
  };
  
  const handlePauseResume = () => {
    setIsPaused(!isPaused);
  };
  
  const handleReset = () => {
    setIsActive(false);
    setTime(0);
  };

    return(
        <>
            <Wrapper>
                <Tab> 
                  <p>Guess Who ?</p>
                  <p>Player : {name}</p>
                  <div>
                  <span>Timer : </span>
                    <span className="digits">
                      {("0" + Math.floor((time / 60000) % 60)).slice(-2)}:
                    </span>
                    <span className="digits">
                      {("0" + Math.floor((time / 1000) % 60)).slice(-2)}
                    </span>
                  </div>
                  <Buttons>
                    <Button onClick={() => navigate("/")}>Home</Button>
                    <Button>Abort</Button>
                    <Button onClick={() => handlePauseResume()}>{isPaused ? "Resume" : "Pause"}</Button>
                  </Buttons>
                </Tab>
                
            </Wrapper>
        </>
    );
}