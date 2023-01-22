import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import { useSelector } from 'react-redux';
import { useNavigate } from "react-router-dom";
import { borderLeft } from "@mui/system";


const Tab = styled.div`
  width: 100%;
  height: 100%;
  font-size: 22px;
  text-align: center;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;

  .title {
    font-size: 30px;
    font-weight: 500;
    border-top : 3px solid #FFFFFF;
    border-bottom : 3px solid #FFFFFF;
  }
`;

const Wrapper = styled.div`
  height: 100%;
  background: #D5E9DC;
  display: flex;
  position: relative;
  height: inherit;
  width: inherit;
`;

const Button = styled.button`
  width: 194px;
  height: 70px;
  font-size: 34px;
  font-weight: 500;
  border-radius: 5px;
  margin-bottom: 20px;
  &: hover {
    cursor: pointer;
  }
`;

const Buttons = styled.div`
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
`;



export default function RightTab(props) {

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

  //console.log(props.questions)

    return(
        <>
            <Wrapper>
                <Tab>
                  <p class="title">Guess Who ?</p>
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
                  <p>Last questions</p>
                  {Object.keys(props.questions).map((key, i) => 
                  
                  (props.questions[key]===true && <p style={{fontWeight: '800'}} key={i+1}>{key} : YES</p>) ||
                  (props.questions[key]===false && <p style={{fontWeight: '800'}} key={i+1}>{key} : NO</p>)
                  ||
                  (props.questions[key]==="" && <p style={{fontWeight: '800'}} key={i+1}>{key} : </p>)
                  )}

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