import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function MultipleImageUpload() {
  const [filesList, setFiles] = useState();
  const images = filesList ? [...filesList] : [];

  const navigate = useNavigate();


  const id_user = localStorage.getItem('id_user')
  const id_partie = localStorage.getItem(id_user)

  const handleChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleUpload = () => {
    const formData = new FormData();
    filesList.map((file, i) => {
      formData.append(`file-${i}`, file)
    })

    const JSONdata = JSON.stringify({
      title: 'get_labels',
      user: id_user,
      id_partie: id_partie,
    })

    formData.append('data', JSONdata)


    // Send to Flask
    fetch(`http://localhost:5000/sent`, {
      method: 'POST',
      body: formData,
      contentType: false,
      processData: false
    })
      .then((res) => {
        res.json()
        navigate("/mode");
      })
      .catch(error => console.log(error))

  };


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