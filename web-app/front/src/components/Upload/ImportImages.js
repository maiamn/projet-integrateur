import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

export default function MultipleImageUpload() {
  const [filesList, setFiles] = useState();
  const navigate = useNavigate();

  const handleChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleUpload = () => {
    const formData = new FormData();
    filesList.map((file,i) => {
      formData.append(`file-${i}`, file)
    })

    const JSONdata = JSON.stringify({
        id_player: 'blabla',
      })
      
    formData.append('data', JSONdata)

    // Send to Flask
    fetch(`http://localhost:5000/add`, {
        method: 'POST',
        body: formData,
        contentType: false,
        processData: false
    })
    .then ((res) => res.json())

    navigate("/mode");
  };

  const images = filesList ? [...filesList] : [];

    return (
      <div>
      <input type="file" onChange={handleChange} multiple />

      <ul>
        {images.map((file, i) => (
          <li key={i}>
            {file.name} - {file.type}
          </li>
        ))}
      </ul>

      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}