import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import Button from "../general/Button";
import Input from "../general/Input_file";


export default function MultipleImageUpload(props) {
  const [filesList, setFiles] = useState();
  const images = filesList ? [...filesList] : [];

  const navigate = useNavigate();


  const id_user = localStorage.getItem('id_user')
  const id_partie = localStorage.getItem(id_user)

  const fileInput = useRef(null)

  const handleChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleUpload = () => {
    const formData = new FormData();
    filesList.map((file, i) => {
      formData.append(`file-${i}.jpg`, file)
    })

    const JSONdata = JSON.stringify({
      title: 'get_labels',
      user: id_user,
      id_partie: id_partie,
    })

    formData.append('data', JSONdata)


    // Send to Flask
    props.setIsLoading(true)

    fetch(`http://localhost:5000/sent`, {
      method: 'POST',
      body: formData,
      contentType: false,
      processData: false
    })
      .then((res) => {
        res.json()
        localStorage.setItem('mode_image', 'upload')
        props.setIsLoading(false)
        navigate("/mode");
      })
      .catch(error => console.log(error))


  };


  return (
    <div style={{ 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center' }}>

      {filesList && <Button type="button" onClick={handleUpload}>Upload</Button>}
      {filesList == undefined &&
        <>
          <Button
            className='button'
            onClick={() => fileInput.current.click()}
          >Select Images to upload</Button>
          <input
            type='file'
            name='image'
            ref={fileInput}
            onChange={handleChange}
            style={{ display: 'none' }}
            multiple
          />

        </>
      }

      <ul>
        {images.map((file, i) => (
          <li key={i}>
            {file.name} - {file.type}
          </li>
        ))}
      </ul>

    </div>
  );
}