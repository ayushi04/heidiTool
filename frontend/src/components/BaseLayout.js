import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation

function BaseLayout({ children }) {
  return (
    <div>
      <header>
        <nav className="navbar navbar-expand-lg navbar-inverse bg-primary bg-faded sticky-top">
          <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <Link className="navbar-brand" to="/">Intensive Visual Analytics Tool</Link>

          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/contact">Contact Us</Link>
              </li>
              {/* Add conditional rendering for user authentication */}
              <li className="nav-item">
                <Link className="nav-link" to="/account">My Account</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/logout">Logout</Link>
              </li>
            </ul>
          </div>
        </nav>
      </header>

      <main className="container mt-5">
        {children}
      </main>

      <footer>
        {/* Add footer content here */}
      </footer>

      {/* Include your JavaScript dependencies here */}
      {/* You can use React's state and useEffect to handle scripts */}
    </div>
  );
}

export default BaseLayout;
