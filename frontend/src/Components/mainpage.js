import Table from 'react-bootstrap/Table';
import Navbar from './navigation';
import { Link } from "react-router-dom";
import React, { useState, useEffect } from "react";
import Data from "../data/mock.json";
import Data1 from "../data/running.json";
  import { Redirect } from 'react-router'; 
import Node1 from "./Node1.js";
import Node2 from "./Node2.js";
import Node3 from "./Node3.js";
import Node4 from "./Node4.js";
import { render } from 'react-dom';





function MainPage() {
  
 
  

  


  
  //const [data, setData] = useState([]);
  const [query, setQuery] = useState("");
  
  // const apiGet = () => {
  //   fetch("https://jsonplaceholder.typicode.com/posts")
  //     .then((response) => response.json())
  //     .then((json) => {
  //       console.log(json);
  //       setData(json);
  //     });
  //   };
  
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);
  
  const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };

   const downloadTxtFile = () => {
   const element = document.createElement("a");
   const file = new Blob([document.getElementById('input').value],    
               {type: 'text/plain;charset=utf-8'});
   element.href = URL.createObjectURL(file);
   element.download = "a.txt";
   document.body.appendChild(element);
   element.click();
   }
  
  
  const handleSubmission = () => {
		const formData = new FormData();

		formData.append('File', selectedFile);

		fetch(
			'https://httpbin.org/post', //some random post api for file upload
			{
				method: 'POST',
				body: formData,
			}
		)
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result);
			})
			.catch((error) => {
				console.error('Error:', error);
			});
  };
  
  const reload = () => {
    <script>
      location.reload();
    </script>
  };
	
    
  const handleClick = async () => {
  const date = new Date();

      <script>
  const myFunction() {
    document.getElementById("innerHTMLdemo").innerHTML = Date()
  };
</script>
    return date;
      
  };
    
  const handleClick1 = async () => {
  const date = new Date();

      <script>
  const myFunction() {
    document.getElementById("innerHTMLdemo1").innerHTML = Date()
  };
</script>
    return date;
      
    };
    
    

    return (
     <div>
        <Navbar />
        <br></br>
        <br></br>


       
  


       
       
       
      {/* <div>
          
          Nodes: {data.map(item => (
        <div key={item.id}>
          <li>{item.userId}</li>
          <li>{item.title}</li>
          </div>
        
          ))}
            
      </div> */}
        


          <table className="table">
            <thead>
              <tr>
                <th>S.N</th>
                <th>Running Nodes</th>
                <th>Status</th>
                    
              </tr>
            </thead>
            <tbody>
              {
                Data1.map(post1 => (
                    
                  <tr key={post1.id}>
                    <td>{post1.id}</td>
                    <td><Link to = {post1.Node_name}>{post1.Node_name}</Link></td>
                    <td>{post1.Status}</td>
                    
                  </tr>
                )
                )
              }
            </tbody>
          </table>
        
        <br></br>
        <br></br>
        <br></br>
        <br></br>

      
      
      <div align ="center">
          <input placeholder="Search the File Name" onChange={event => setQuery(event.target.value)} />
          <a href="/download" download="a.txt">
  Download file 
          </a>
      </div>

        
        {
          Data.filter(post => {
            if (query === '') {
              return null;
            } else if (post.File_name.toLowerCase().includes(query.toLowerCase())) {
              return post;
            }
          }).map((post, index) => (
    <div className="box" key={index}>
              <p><b>{post.Node_name}</b></p>
               <p><b>{post.File_name}</b></p>
                <p><b>{post.ip_address}</b></p>
    </div>
     ))
        }

        <div>
			<input type="file" name="file" onChange={changeHandler} />
			{isFilePicked ? (
				<div>
					<p>Filename: {selectedFile.name}</p>
					<p>Filetype: {selectedFile.type}</p>
					<p>Size in bytes: {selectedFile.size}</p>
					<p>
						lastModifiedDate:{' '}
						{selectedFile.lastModifiedDate.toLocaleDateString()}
					</p>
				</div>
			) : (
				<p>Select a file to show details</p>
			)}
			<div>
				<button onClick={handleSubmission}>upload</button>
			</div>
		</div>
        {/* <div align="center">
          <h4>List of Files</h4>
      
          <ul align="left">
            <li><a href='*'>File1.txt</a></li>
            <li><a href='*'>File2.txt</a></li>
            <li><a href='*'>File3.txt</a></li>
          </ul>

        </div> */}
      </div>
      
    );
  
}

export default MainPage;
