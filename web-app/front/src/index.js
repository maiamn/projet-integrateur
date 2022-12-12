import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './MainPage';
import reportWebVitals from './reportWebVitals';
import store from './redux/store'
import { Provider } from 'react-redux'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./MainPage"
import ChooseImage from "./ChooseImage"
import Question_vPlayer from "./Question_vPlayer";
import ChooseMode from "./ChooseMode";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
     
    <BrowserRouter>
      <Routes>
        <Route path="/image" element={<ChooseImage />}/>
        <Route path="/question" element={<Question_vPlayer />}/>
        <Route path="/" element={<MainPage />}/>
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
