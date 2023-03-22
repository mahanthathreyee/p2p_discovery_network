import Table from 'react-bootstrap/Table';
import Navbar from './navigation';
import React, { useState, useEffect } from "react";




  //Get Method
  


function Node1() { 

  const [date, setDate] = useState(new Date());
  
  useEffect(() => {
        var timer = setInterval(()=>setDate(new Date()), 1000 )
        return function cleanup() {
            clearInterval(timer)
        }
    
    });

  return ( 
    
    <div>
      <Navbar />
     
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
          <th>#</th>
          <th>Node List</th>
            <th>Time</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td><a href="*"> Node 1</a></td>
          <td>{date.toLocaleTimeString()}</td>
          <td>running</td>
        </tr>
        <tr>
          <td>2</td>
          <td><a href="*"> Node 2</a></td>
          <td>{date.toLocaleTimeString()}</td>
          <td>running</td>
        </tr>
        <tr>
          <td>3</td>
          <td><a href="*"> Node 3</a></td>
            <td>{date.toLocaleTimeString()}</td>
            <td>running</td>
          </tr>
          <tr>
          <td>4</td>
          <td><a href="*"> Node 4</a></td>
            <td>{date.toLocaleTimeString()}</td>
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
          <li><a href="/" download="a.txt">
            a.txt
          </a></li>
          <li><a href="/" download="b.txt">
            b.txt
          </a></li>
          <li><a href="/" download="c.txt">
            c.txt 
          </a></li>  
        </ul>

      </div>
      </div>
      
  );
}

export default Node1;
