import React, { useState, useEffect } from 'react';

function Cities() {
  const [cities, setCities] = useState([]);
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/cities');
      const data = await response.json();
      setCities(data);
    } catch (error) {
      console.error('Error fetching cities:', error);
    }
  };

  const getWeather = async (city) => {
    try {
      const response = await fetch(`http://localhost:5000/api/weather/${city}`);
      if (response.ok) {
        const data = await response.json();
        setWeather(data);
      }
    } catch (error) {
      console.error('Error fetching weather:', error);
    }
  };

  return (
    <div className="container">
      <h2>Available Cities</h2>
      <div className="cities-grid">
        {cities.map((city, index) => (
          <div key={index} className="city-item clickable" onClick={() => getWeather(city)}>
            {city}
          </div>
        ))}
      </div>
      
      {weather && (
        <div className="weather-card">
          <h2>{weather.city}</h2>
          <div className="current-weather">
            <div className="temp">{weather.temperature}°C</div>
            <div className="description">{weather.condition}</div>
            <div className="details">
              <span>Humidity: {weather.humidity}%</span>
              <span>Wind: {weather.wind_speed} m/s</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Cities;