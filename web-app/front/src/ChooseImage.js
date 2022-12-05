import React, { useState, useEffect } from "react";
import styled from 'styled-components';

const Button = styled.button`
  background: #D9D9D9;
  border: 2px solid #D9D9D9;
  width: 413px;
  height: 100px;
  font-size: 34px;
  &: hover {
    cursor: pointer;
    border: 2px solid #000000;
  }
`;

const Title = styled.h1`

  width: 603px;
  height: 73px;

  font-style: normal;
  font-weight: 600;
  font-size: 64px;
  line-height: 77px;
  text-align: center;
  text-transform: uppercase;
`;

export default function ChooseImage() {
    return(
        <>
            <Title>What pictures do you want to play with ?</Title>
            <Button type="button">
                Random
            </Button>
            <Button type="button">
                Upload from computer
            </Button>
        </>
    );
}
