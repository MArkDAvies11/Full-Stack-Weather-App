import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav className="navigation">
      <h1>Weather App</h1>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/users">Users</Link>
        <Link to="/favorites">Favorites</Link>
        <Link to="/cities">Cities</Link>
      </div>
    </nav>
  );
}

export default Navigation;