import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

/*export default function MultipleImageUpload() {
  const [image, setImage] = useState();

  const handleChange = (event) => {
    setImage(event.target.files[0]);
  };*/
class Upload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null,
            uploading: false
        };
        this.handleUpload = this.handleUpload.bind(this);
    }
    
  async handleUpload (event) {

    const files = Array.from(event.target.files);
    const formData = new FormData();
    files.map((file, index) =>{
      formData.append(`file${index}`, file);
    })
    // formData.append("file", files[0]); // key - value

    // Send to Flask
    const response = await fetch(`http://localhost:5000/add`, {
        method: 'POST',
        body: formData,
        contentType: false,
        processData: false
    });
    const data = await response.json();
    console.log(data);
    this.setState({
        file: `data:image/jpeg;base64, ${data['data']}`,
        uploading: true
    });

    /*const formData = new FormData();
    formData.append("image", image, image.name);*/

    /* fetch("http://localhost:5000/add", {
      method: "POST",
      body: image,
      /*headers: {
        "content-type": image.type,
        "content-length": `${image.size}`,
      },
      
    })
      .then((res) => console.log(res))

      .catch((err) => console.error(err));
  };*/
}

  render() {
    return (
      /*<div>
        <input type="file" onChange={handleChange} />
        <div>{image && `${image.name} - ${image.type} - ${image.size}`}</div>
        <button onClick={handleUpload}>Upload Image</button>
      </div>*/
      <div>
        <input type="file" multiple />
        <button onClick={this.handleUpload}>Upload Image</button>
        <br />
        { this.state.file && <img src={this.state.file} alt="jeye"/> }
      </div>
  );
}
}

/* module.exports = Upload; */
export default Upload;
