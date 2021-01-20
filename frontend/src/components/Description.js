import React from 'react'
import 'w3-css/w3.css';

function Description(){

  return(
    <div className="w3-content">  
        <p>
          Neural style transfer is an optimization technique used to take three images, a content image, 
          a style reference image (such as an artwork by a famous painter), and the input image you want to style — 
          and blend them together such that the input image is transformed to look like the content image, but “painted” in the style of the style image.
        </p>
        <p>For example, let’s take an image of this turtle and Katsushika Hokusai’s The Great Wave off Kanagawa:</p>
        <img className="w3-center"  width="512" src="https://miro.medium.com/max/874/0*h5YONGux0M4j1Bdf" />
        <img width="224" src="https://miro.medium.com/max/850/0*qdJ0aARvEcEuJ92l" />
        <p>Now how would it look like if Hokusai decided to add the texture or style of his waves to the image of the turtle? Something like the picture on top right?</p>
        <p>Is this magic or just deep learning? Fortunately, this doesn’t involve any magic: style transfer is a fun and interesting technique that showcases the capabilities and internal representations of neural networks.</p>
    </div>
  )

}
export default Description;
