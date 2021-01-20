import React, { useState } from 'react'
import { useForm } from 'react-hook-form';
import 'w3-css/w3.css';

function Demo(){

  const {register,handleSubmit} = useForm()
  const [image,setImage] = useState(" ")
  const [source,setSource] = useState(" ")

  const Example = ({ data }) => <img width="256" src={image} alt="Image here" />

  const onSubmit = (data) => {

    setSource(URL.createObjectURL(data.image[0]))
    console.log(data)
    const formData = new FormData();
    formData.append('file', data.image[0]);

    console.log(formData) 

    const options = {
      method: 'POST',
      body: formData,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
     };

    fetch('http://127.0.0.1:5000/predict', options)
      .then(res => res.json())
      .then(resj => setImage(resj.url))
  }

  console.log(Image)
  return(
    <div className="w3-content">
        <h3><b>Try the Algorithm!</b></h3>
        <form onSubmit={handleSubmit(onSubmit)}>
          <input ref={register} type="file" name="image" />
          <br />
          <button className="w3-button w3-black w3-margin">Submit</button>
        </form>
        <div className="w3-card-4 w3-center">
          <img src={source} width="256" />
          <span className="w3-padding">
            <Example data={Image} />
          </span>
        </div>
    </div>
  )

}
export default Demo;
