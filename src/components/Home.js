import React, { useState } from 'react';

function Home() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);

  const getWeather = async () => {
    if (!city.trim()) return;

    try {
      const [weatherResponse, forecastResponse] = await Promise.all([
        fetch(`http://127.0.0.1:5000/api/weather/${city}`),
        fetch(`http://127.0.0.1:5000/api/forecast/${city}`)
      ]);
      
      if (!weatherResponse.ok) throw new Error('City not found');

      const weatherData = await weatherResponse.json();
      const forecastData = await forecastResponse.json();
      
      setWeather(weatherData);
      setForecast(forecastData);
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

      {forecast && (
        <div className="forecast">
          <h3>5-Day Forecast</h3>
          <div className="forecast-cards">
            {forecast.forecast.map((day, index) => (
              <div key={index} className="forecast-card">
                <div className="date">{new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}</div>
                <div className="temp">{day.temperature}°C</div>
                <div>{day.condition}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;