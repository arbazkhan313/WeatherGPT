import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  Search,
  Send,
  MapPin,
  Thermometer,
  Droplets,
  Wind,
  Gauge,
  CloudSun,
  CalendarDays,
  History,
  Sparkles,
} from "lucide-react";

import "./App.css";


function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);


  const askWeatherGPT = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const url = `http://127.0.0.1:8000/agent/ask?question=${encodeURIComponent(
        question
      )}`;

      const res = await fetch(url);
      const data = await res.json();

      setResponse(data);
    } catch (error) {
      setResponse({
        success: false,
        message: "Unable to connect to WeatherGPT backend.",
      });
    }

    setLoading(false);
  };


  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askWeatherGPT();
    }
  };


  const quickQuestion = (text) => {
    setQuestion(text);
  };


  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            <CloudSun size={25} />
          </div>

          <div>
            <h1>WeatherGPT</h1>
            <p>AI Weather Intelligence</p>
          </div>

        </div>


        <div className="location-pill">
          <MapPin size={17} />
          <span>Mandya, Karnataka</span>
        </div>

      </header>


      {/* MAIN */}

      <main className="main">

        <section className="hero">

          <div className="hero-icon">
            <Sparkles size={22} />
          </div>

          <h2>
            Your AI Weather
            <span> Intelligence</span>
          </h2>

          <p>
            Ask anything about weather, forecasts and historical trends.
          </p>


          {/* SEARCH */}

          <div className="search-box">

            <Search size={21} />

            <input
              type="text"
              placeholder="Ask WeatherGPT anything..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
            />

            <button
              onClick={askWeatherGPT}
              disabled={loading}
            >
              {loading ? (
                "..."
              ) : (
                <Send size={19} />
              )}
            </button>

          </div>


          {/* QUICK QUESTIONS */}

          <div className="quick-questions">

            <button
              onClick={() =>
                quickQuestion("What is the temperature in Mandya?")
              }
            >
              <Thermometer size={16} />
              Current weather
            </button>


            <button
              onClick={() =>
                quickQuestion("What is the forecast for Mandya?")
              }
            >
              <CalendarDays size={16} />
              Forecast
            </button>


            <button
              onClick={() =>
                quickQuestion(
                  "What was the weather like in Mandya last year?"
                )
              }
            >
              <History size={16} />
              Historical
            </button>

          </div>

        </section>


        {/* LOADING */}

        {loading && (
          <div className="loading-card">

            <div className="loader"></div>

            <p>
              WeatherGPT is analyzing your question...
            </p>

          </div>
        )}


        {/* SUCCESS RESPONSE */}

        {response && response.success && (

          <section className="result-section">

            {/* LOCATION */}

            <div className="result-location">

              <div>

                <MapPin size={18} />

                <strong>
                  {response.location?.name}
                </strong>

                <span>
                  {response.location?.state}
                  {response.location?.state && ", "}
                  {response.location?.country}
                </span>

              </div>

              <span className="intent-badge">
                {response.intent}
              </span>

            </div>


            {/* CURRENT WEATHER */}

            {response.weather && (

              <div className="weather-grid">

                <div className="weather-card">

                  <Thermometer />

                  <span>
                    Temperature
                  </span>

                  <strong>
                    {response.weather.temperature}°C
                  </strong>

                  <small>
                    Feels like {response.weather.feels_like}°C
                  </small>

                </div>


                <div className="weather-card">

                  <Droplets />

                  <span>
                    Humidity
                  </span>

                  <strong>
                    {response.weather.humidity}%
                  </strong>

                  <small>
                    Relative humidity
                  </small>

                </div>


                <div className="weather-card">

                  <Wind />

                  <span>
                    Wind
                  </span>

                  <strong>
                    {response.weather.wind_speed} m/s
                  </strong>

                  <small>
                    Current wind speed
                  </small>

                </div>


                <div className="weather-card">

                  <Gauge />

                  <span>
                    Pressure
                  </span>

                  <strong>
                    {response.weather.pressure}
                  </strong>

                  <small>
                    hPa
                  </small>

                </div>

              </div>

            )}


            {/* FORECAST */}

            {response.forecast && (

              <div className="forecast-card">

                <div className="section-title">

                  <CalendarDays size={19} />

                  <h3>
                    Upcoming Forecast
                  </h3>

                </div>


                <div className="forecast-list">

                  {response.forecast.forecast
                    ?.slice(0, 6)
                    .map((item, index) => (

                      <div
                        className="forecast-item"
                        key={index}
                      >

                        <span>
                          {item.datetime}
                        </span>

                        <strong>
                          {item.temperature}°C
                        </strong>

                        <small>
                          {item.weather}
                        </small>

                      </div>

                    ))}

                </div>

              </div>

            )}


            {/* HISTORICAL WEATHER */}

            {response.summary && (

              <div className="forecast-card">

                <div className="section-title">

                  <History size={19} />

                  <h3>
                    Historical Summary — {response.summary.year}
                  </h3>

                </div>


                <div className="history-grid">

                  <div>

                    <span>
                      Average
                    </span>

                    <strong>
                      {response.summary.average_temperature}°C
                    </strong>

                  </div>


                  <div>

                    <span>
                      Maximum
                    </span>

                    <strong>
                      {response.summary.maximum_temperature}°C
                    </strong>

                  </div>


                  <div>

                    <span>
                      Minimum
                    </span>

                    <strong>
                      {response.summary.minimum_temperature}°C
                    </strong>

                  </div>


                  <div>

                    <span>
                      Rainfall
                    </span>

                    <strong>
                      {response.summary.total_precipitation_mm} mm
                    </strong>

                  </div>

                </div>

              </div>

            )}


            {/* AI ANSWER */}

            <div className="ai-answer">

              <div className="answer-header">

                <div className="ai-icon">
                  <Sparkles size={18} />
                </div>

                <div>

                  <h3>
                    WeatherGPT Insight
                  </h3>

                  <span>
                    AI-generated from weather data
                  </span>

                </div>

              </div>


              {/* GITHUB-FLAVORED MARKDOWN */}

              <div className="ai-answer-content">

                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {response.answer}
                </ReactMarkdown>

              </div>

            </div>

          </section>

        )}


        {/* ERROR */}

        {response && !response.success && (

          <div className="error-card">

            <strong>
              Something went wrong
            </strong>

            <p>
              {response.message}
            </p>

          </div>

        )}

      </main>


      {/* FOOTER */}

      <footer>

        <span>
          WeatherGPT
        </span>

        <span>
          AI-powered weather intelligence
        </span>

      </footer>

    </div>
  );
}


export default App;