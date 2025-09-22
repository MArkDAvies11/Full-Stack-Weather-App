import React from 'react';

function WeatherDisplay({ weather }) {
  if (!weather) return null;

  return (
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
  );
}

export default WeatherDisplay;