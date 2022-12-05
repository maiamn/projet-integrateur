import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./MainPage"
import ChooseImage from "./ChooseImage"
import Question_vPlayer from "./Question_vPlayer";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />}/>
        <Route path="/image" element={<ChooseImage />}/>
        <Route path="/question" element={<Question_vPlayer />}/>
      </Routes>
    </BrowserRouter>
  );
}
