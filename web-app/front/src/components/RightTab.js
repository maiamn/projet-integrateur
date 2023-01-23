import React, { useState } from "react";
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
  padding-top:20px;
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Questions = styled.div`
  padding-bottom: 10px;
  overflow: auto;
`;

export default function RightTab(props) {

  const [isPaused, setIsPaused] = useState(false);

  const [time, setTime] = useState(0);
  const name = localStorage.getItem('id_user')
  const navigate = useNavigate();



  React.useEffect(() => {
    let interval = null;

    if (isPaused === false) {
      interval = setInterval(() => {
        setTime((time) => time + 10);
      }, 10);
    } else {
      clearInterval(interval);
    }
    return () => {
      clearInterval(interval);
    };
  }, [isPaused]);



  const handlePauseResume = () => {
    setIsPaused(!isPaused);
  };

  const handleStop = () => {
    let user = localStorage.getItem('id_user')
    let partie = localStorage.getItem(user)

    localStorage.clear()

    localStorage.setItem('id_user', user)
    localStorage.setItem(user, partie)
    navigate('/')
  };


  return (
    <>
      <Wrapper>
        <Tab>
          <p class="title">Guess Who ?</p>
          <p style={{ fontSize: '25px' }}>Player : {name}</p>
          <div>
            <span style={{ fontSize: '25px' }}>Timer : </span>
            <span style={{ fontSize: '25px' }} className="digits">
              {("0" + Math.floor((time / 60000) % 60)).slice(-2)}:
            </span>
            <span style={{ fontSize: '25px' }} className="digits">
              {("0" + Math.floor((time / 1000) % 60)).slice(-2)}
            </span>
          </div>
          <p style={{ fontSize: '25px' }}>Last questions</p>
          <Questions>
            {Object.keys(props.questions).map((key, i) =>

              (props.questions[key] === true && <p style={{ fontSize: '20px', textAlign: 'left', paddingLeft: "20px", fontWeight: '800' }} key={i + 1}>{key} YES</p>) ||
              (props.questions[key] === false && <p style={{ fontSize: '20px', textAlign: 'left', paddingLeft: "20px", fontWeight: '800' }} key={i + 1}>{key} NO </p>)
              ||
              (props.questions[key] === "" && <p style={{ fontSize: '20px', textAlign: 'left', paddingLeft: "20px", fontWeight: '800' }} key={i + 1}>{key}  </p>)

            )}
          </Questions>

          <Buttons>
            <Button onClick={() => handleStop()}>Stop</Button>
            <Button onClick={() => handlePauseResume()}>{isPaused ? "Resume" : "Pause"}</Button>
          </Buttons>
        </Tab>

      </Wrapper>
    </>
  );
}