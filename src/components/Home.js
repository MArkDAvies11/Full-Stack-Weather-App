import React, { useState } from 'react';

function Home() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);

  const getWeather = async () => {
    if (!city.trim()) return;

    try {
      const response = await fetch(`http://localhost:5000/api/weather/${city}`);
      
      if (!response.ok) throw new Error('City not found');

      const weatherData = await response.json();
      setWeather(weatherData);
    } catch (error) {
      alert('City not found. Please try again.');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      getWeather();
    }
  };

  return (
    <div className="container">
      <div className="search-box">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter city name"
        />
        <button onClick={getWeather}>Search</button>
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

export default Home;