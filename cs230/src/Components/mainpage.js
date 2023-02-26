import Table from 'react-bootstrap/Table';
import Navbar from './navigation';
import { Link } from "react-router-dom";
import React, { useState, useEffect } from "react";
  import { Redirect } from 'react-router'; 
import Node1 from "./Node1.js";
import { render } from 'react-dom';

  //Get Method
  


class MainPage extends React.Component {


  render() {
    
    
    const apiGet = () => {
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        //setData(json.id);
      });
    };
    
  const handleClick = async () => {
  const date = new Date();

      
      console.log(date);
      
    };
    
    

    return (
      <div>
        <Navbar />
        <button onClick={apiGet}>Fetch API</button>
       
        {/* <div>
        <ul>
          {data.map((item) => (
            <li key={item.id}>
              {item.userId},{item.title}
            </li>
          ))}
        </ul>
      </div> */}
        <Table striped bordered hover size="sm">
          <thead>
            <tr>
              <th>ip</th>
              <th>Node List</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>192.78.1.11</td>
              <td><Link to='/Node1'>Node1</Link> <button onClick={handleClick}></button></td>
             
              <td>11:00</td>
              <td>running</td>
            </tr>
            <tr>
              <td>192.78.1.22</td>
              <td><a href="*"> Node 2</a></td>
              <td>11:05</td>
              <td>running</td>
            </tr>
            <tr>
              <td>192.78.3.22</td>
              <td><a href="*"> Node 3</a></td>
              <td>12:05</td>
              <td>running</td>
            </tr>
            <tr>
              <td>192.78.4.21</td>
              <td><a href="*"> Node 4</a></td>
              <td>12:40</td>
              <td>running</td>
            </tr>
          </tbody>
        </Table>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
      
        <div align="center">
          <h4>List of Files</h4>
      
          <ul align="left">
            <li><a href='*'>File1.txt</a></li>
            <li><a href='*'>File2.txt</a></li>
            <li><a href='*'>File3.txt</a></li>
          </ul>

        </div>
      </div>
      
    );
  }
}

export default MainPage;