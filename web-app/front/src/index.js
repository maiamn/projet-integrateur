import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import store from './redux/store'
import { Provider } from 'react-redux'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./MainPage"
import ChooseImage from "./ChooseImage"
import ChooseMode from "./ChooseMode";
import Question_vComputer from './Question_vComputer';
import Show_Images from './Show_Images';
import Fin_vPlayer from './Fin_vPlayer';
import Jeu_vPlayer from './Jeu_vPlayer';
import Show_Images_Computer from './Show_Images_Computer';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>

      <BrowserRouter>
        <Routes>
          <Route path="/image" element={<ChooseImage />} />
          <Route path="/question_computer" element={<Question_vComputer />} />
          <Route path="/show_images" element={<Show_Images />} />
          <Route path="/show_images_computer" element={<Show_Images_Computer />} />
          <Route path="/fin_player" element={<Fin_vPlayer />} />
          <Route path="/jeu_player" element={<Jeu_vPlayer />} />
          <Route path="/" element={<MainPage />} />
          <Route path="/mode" element={<ChooseMode />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
