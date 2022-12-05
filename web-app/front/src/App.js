import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./MainPage";
import ChooseImage from "./ChooseImage";
import ChooseMode from "./ChooseMode";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/image" element={<ChooseImage />} />
        <Route path="/mode" element={<ChooseMode />} />
      </Routes>
    </BrowserRouter>
  );
}
