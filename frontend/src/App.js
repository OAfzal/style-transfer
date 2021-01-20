import React from 'react';
import 'w3-css/w3.css';
import Header from './components/Header.js';
import Description from './components/Description.js';
import Demo from './components/Demo.js';
import Footer from './components/Footer.js'

function App(){

  return(
    <div className="w3-padding-large">
      <Header  />
      <Description style="height:300px;" />
      <Demo/>
    </div>
  )

}
export default App;
