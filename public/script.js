async function getWeather() {
    const city = document.getElementById('cityInput').value.trim();
    if (!city) return;

    try {
        const [weatherResponse, forecastResponse] = await Promise.all([
            fetch(`/api/weather/${city}`),
            fetch(`/api/forecast/${city}`)
        ]);

        if (!weatherResponse.ok) throw new Error('City not found');

        const weatherData = await weatherResponse.json();
        const forecastData = await forecastResponse.json();

        displayWeather(weatherData);
        displayForecast(forecastData);
    } catch (error) {
        alert('City not found. Please try again.');
    }
}

function displayWeather(data) {
    document.getElementById('cityName').textContent = data.name;
    document.getElementById('temperature').textContent = `${Math.round(data.main.temp)}°C`;
    document.getElementById('description').textContent = data.weather[0].description;
    document.getElementById('humidity').textContent = `Humidity: ${data.main.humidity}%`;
    document.getElementById('windSpeed').textContent = `Wind: ${data.wind.speed} m/s`;
    
    document.getElementById('weatherResult').classList.remove('hidden');
}

function displayForecast(data) {
    const forecastCards = document.getElementById('forecastCards');
    forecastCards.innerHTML = '';

    const dailyData = data.list.filter((item, index) => index % 8 === 0).slice(0, 5);

    dailyData.forEach(day => {
        const date = new Date(day.dt * 1000);
        const card = document.createElement('div');
        card.className = 'forecast-card';
        card.innerHTML = `
            <div class="date">${date.toLocaleDateString('en-US', { weekday: 'short' })}</div>
            <div class="temp">${Math.round(day.main.temp)}°C</div>
            <div>${day.weather[0].description}</div>
        `;
        forecastCards.appendChild(card);
    });

    document.getElementById('forecast').classList.remove('hidden');
}

document.getElementById('cityInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        getWeather();
    }
});