
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import './App.css';
import BaseLayout from './components/BaseLayout'; // Import BaseLayout component from the correct path
import Home from './pages/Home'; // Import Home component from the correct path
import Contact from './components/Contact'; // Import Contact component from the correct path
import ColumnsDisplay  from './components/ColumnsDisplay';
import Heidi  from './pages/Heidi';

function App() {
  return (
    <Router>
      <div>
        {/* Use BaseLayout as a wrapper around your content */}
        <BaseLayout>
          <Routes>
            <Route path="/columns" element={<ColumnsDisplay />} />
            <Route exact path="/heidi" element={<Heidi />} />
            <Route exact path="/" element={<Home />} />
            {/* <Route path="/contact" component={Contact} /> */}
            {/* Add more routes for other pages */}
          </Routes>
        </BaseLayout>
      </div>
    </Router>
  );
}

export default App;
