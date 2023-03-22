import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <a className="navbar-brand">
        
          CS 230
        
        
      </a>
      
      <div className="collapse navbar-collapse" id="navbarNavDropdown">
        <ul className="navbar-nav">
          <li className="nav-item active">
            <a className="nav-link">
              <Link to='/'>
                Home
              </Link>
               
            </a>
          </li>
          <li className="nav-item active">
            <a className="nav-link">
              <Link to='/Node1'>
                Node1
              </Link>
               
            </a>
          </li>
          <li className="nav-item active">
            <a className="nav-link">
              <Link to='/Node2'>
                Node2
              </Link>
               
            </a>
          </li>
          <li className="nav-item active">
            <a className="nav-link">
              <Link to='/Node3'>
                Node3
              </Link>
               
            </a>
          </li>
                {/* <li className="nav-item">
            <a className="nav-link" href="#">
              
            </a>
          </li> */}
          {/* <li className="nav-item">
            <a className="nav-link" href="#">
              Pricing
            </a>
          </li> */}
          {/* <li className="nav-item dropdown">
            <a
              className="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdownMenuLink"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Dropdown link
            </a>
            <div
              className="dropdown-menu"
              aria-labelledby="navbarDropdownMenuLink"
            >
              <a className="dropdown-item" href="#">
                Action
              </a>
              <a className="dropdown-item" href="#">
                Another action
              </a>
              <a className="dropdown-item" href="#">
                Something else here
              </a>
            </div>
          </li> */}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
