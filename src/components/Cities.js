import React, { useState, useEffect } from 'react';

function Cities() {
  const [cities, setCities] = useState([]);
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/cities');
      const data = await response.json();
      setCities(data);
    } catch (error) {
      console.error('Error fetching cities:', error);
    }
  };

  const getWeather = async (city) => {
    try {
      const [weatherResponse, forecastResponse] = await Promise.all([
        fetch(`http://127.0.0.1:5000/api/weather/${city}`),
        fetch(`http://127.0.0.1:5000/api/forecast/${city}`)
      ]);
      
      if (weatherResponse.ok && forecastResponse.ok) {
        const weatherData = await weatherResponse.json();
        const forecastData = await forecastResponse.json();
        setWeather(weatherData);
        setForecast(forecastData);
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

export default Cities;