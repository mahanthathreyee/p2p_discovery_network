import './App.css';
import Navbar from './Components/navigation';
import { BrowserRouter, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import MainPage from './Components/mainpage.js';
import Node1 from './Components/Node1';

function App(props) {
  return (
    <MainPage />
  )   
  
};

export default App;
