import React, { useState, useEffect } from "react";
import styled from 'styled-components';

const Tab = styled.div`
  width: 349px;
  height: 100%;
  margin-left: auto;
  background: #D9D9D9;
  font-size: 34px;
  text-align: center;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
`;

const Wrapper = styled.div`
  display: flex;
  position: absolute;
  height: 100%;
  width: 100%;
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

    return(
        <>
            <Wrapper>
                <Tab> 
                  <p>Guess Who ?</p>
                  <p>Player : XXXX</p>
                  <p>Timer : XX:XX</p>
                  <Buttons>
                    <Button>Home</Button>
                    <Button>Abort</Button>
                    <Button>Pause</Button>
                  </Buttons>
                </Tab>
                
            </Wrapper>
        </>
    );
}