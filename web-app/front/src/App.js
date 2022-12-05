import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./MainPage"
import ChooseImage from "./ChooseImage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />}/>
        <Route path="/image" element={<ChooseImage />}/>
      </Routes>
    </BrowserRouter>
  );
}
