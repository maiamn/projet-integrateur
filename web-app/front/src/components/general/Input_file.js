import React, { useState, useEffect } from "react";
import styled from "styled-components";

export const Input = styled.file`
background: #D5E9DC;
border: 2px solid #d9d9d9;
box-shadow: 0px .1rem .3rem 0px #bec8e4;;
border-radius: 10px;
text-align: center;
margin: 10px;
width: 350px;
height: 80px;
font-size: 34px;
&: hover {
  cursor: pointer;
  border: 2px solid #ffffff;
  background: #e7f4eb;
}
`;

export default Input;