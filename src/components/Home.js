import React, { useState } from 'react';

function Home() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getWeather = async () => {
    if (!city.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const [weatherResponse, forecastResponse] = await Promise.all([
        fetch(`/api/weather/${encodeURIComponent(city)}`),
        fetch(`/api/forecast/${encodeURIComponent(city)}`)
      ]);
      
      if (!weatherResponse.ok) throw new Error('City not found');

      const weatherData = await weatherResponse.json();
      const forecastData = await forecastResponse.json();
      
      setWeather(weatherData);
      setForecast(forecastData);
    } catch (error) {
      setError('City not found. Please try again.');
      setWeather(null);
      setForecast(null);
    } finally {
      setLoading(false);
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
        <button onClick={getWeather} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="error-message" style={{color: 'red', textAlign: 'center', margin: '20px 0'}}>
          {error}
        </div>
      )}

      {weather && (
        <div className="weather-card">
          <h2>{weather.name}</h2>
          <div className="current-weather">
            <div className="temp">{weather.main.temp}°C</div>
            <div className="description">{weather.weather[0].description}</div>
            <div className="details">
              <span>Humidity: {weather.main.humidity}%</span>
              <span>Wind: {weather.wind.speed} m/s</span>
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