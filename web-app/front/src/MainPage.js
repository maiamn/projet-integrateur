import logo from './logo.png';
import React, { useState, useEffect } from "react";
import './App.css';
import styled from 'styled-components';
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux'
import { update } from './redux/profileSlice'
import loader from './components/Snake.gif'


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

const PlayButton = styled.button`
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

const EnterName = styled.p`
  margin-top: 60px;
  margin-bottom: 10px;
`

const PlayerName = styled.input`
  margin-bottom: 20px;
  background: #D9D9D9;
  width: 320px;
  height: 40px;
  font-size: 20px;
  padding-left: 5px;
`

function MainPage() {

  const [isLoading, setIsLoading] = useState(false)

  const navigate = useNavigate();

  const [data, setdata] = useState({
    image: ""
  });

  const [name, setName] = useState("");

  const dispatch = useDispatch()

  useEffect(() => {
    fetch('http://localhost:5000/db', {
      credentials: "include",
      'methods': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json().then(function (result) {
        setdata({ image: result.data, })
      }))

      .catch(error => console.log(error))

  }, []);


  const handle = (e) => {
    setName(e)
  }


  function test() {
    //id user c'est le current user pour cette partie
    localStorage.setItem('id_user', name)

    // dans le local storage on stocker Emma : 1, Emma a fait 1 partie 
    if (localStorage.getItem(name)) {
      localStorage.setItem(name, JSON.parse(localStorage.getItem(name)) + 1)
    } else {
      localStorage.setItem(name, 1)
    }

    navigate("/image");
    dispatch(update(name));

  }

  return (
    <div className="App">

      <header className="App-header">
        <Title>Guess who ?</Title>
        <img src={logo} className="App-logo" alt="logo" />
        <EnterName>Enter player's name:</EnterName>
        <PlayerName
          type="text"
          value={name}
          onChange={(e) => handle(e.target.value)}
        />
        <PlayButton type="button" onClick={() => {
          test();
        }}>
          Play
        </PlayButton>

      </header>
    </div>
  );
}

export default MainPage;
