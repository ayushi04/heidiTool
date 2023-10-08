
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import './App.css';
import BaseLayout from './components/BaseLayout'; // Import BaseLayout component from the correct path
import Home from './components/Home'; // Import Home component from the correct path
import Contact from './components/Contact'; // Import Contact component from the correct path
import ColumnsDisplay  from './components/ColumnsDisplay';

function App() {
  return (
    <Router>
      <div>
        {/* Use BaseLayout as a wrapper around your content */}
        <BaseLayout>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/contact" component={Contact} />
            <Route path="/columns" component={ColumnsDisplay} />
            {/* Add more routes for other pages */}
          </Switch>
        </BaseLayout>
      </div>
    </Router>
  );
}

export default App;
