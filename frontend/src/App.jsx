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
  ShieldAlert,
  CloudRain,
  CloudLightning,
  Waves,
  AlertTriangle,
} from "lucide-react";

import "./App.css";


function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);


  // =========================================================
  // ASK WEATHERGPT
  // =========================================================

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


  // =========================================================
  // ENTER KEY
  // =========================================================

  const handleKeyDown = (event) => {

    if (event.key === "Enter" && !event.shiftKey) {

      event.preventDefault();

      askWeatherGPT();

    }

  };


  // =========================================================
  // QUICK QUESTION
  // =========================================================

  const quickQuestion = (text) => {

    setQuestion(text);

  };


  // =========================================================
  // RISK ICON
  // =========================================================

  const getRiskIcon = (type) => {

    switch (type) {

      case "heavy_rain":
      case "rain":
      case "precipitation_probability":
        return <CloudRain size={20} />;

      case "thunderstorm":
        return <CloudLightning size={20} />;

      case "flood":
        return <Waves size={20} />;

      case "wind":
      case "forecast_wind":
        return <Wind size={20} />;

      case "heat":
        return <Thermometer size={20} />;

      default:
        return <AlertTriangle size={20} />;

    }

  };


  // =========================================================
  // RISK TYPE FORMATTER
  // =========================================================

  const formatRiskType = (type) => {

    return type
      ?.replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());

  };


  // =========================================================
  // RISK CLASS
  // =========================================================

  const getRiskClass = (level) => {

    if (level === "high") {
      return "risk-high";
    }

    if (level === "moderate") {
      return "risk-moderate";
    }

    return "risk-low";

  };


  // =========================================================
  // FORMAT EVIDENCE KEY
  // =========================================================

  const formatEvidenceKey = (key) => {

    return key
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());

  };


  // =========================================================
  // FORMAT EVIDENCE VALUE
  // =========================================================

  const formatEvidenceValue = (key, value) => {

    if (value === null || value === undefined) {
      return "-";
    }

    if (typeof value !== "number") {
      return value;
    }

    let formattedValue;

    if (Number.isInteger(value)) {
      formattedValue = value;
    } else {
      formattedValue = value.toFixed(2);
    }

    if (key.includes("probability")) {
      return `${formattedValue}%`;
    }

    if (key.includes("temperature")) {
      return `${formattedValue}°C`;
    }

    if (key.includes("rain_amount")) {
      return `${formattedValue} mm`;
    }

    if (key.includes("wind_speed")) {
      return `${formattedValue} m/s`;
    }

    if (key.includes("wind_gust")) {
      return `${formattedValue} m/s`;
    }

    return formattedValue;

  };


  return (

    <div className="app">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            <CloudSun size={25} />
          </div>

          <div>

            <h1>
              WeatherGPT
            </h1>

            <p>
              AI Weather Intelligence
            </p>

          </div>

        </div>


        <div className="location-pill">

          <MapPin size={17} />

          <span>
            Mandya, Karnataka
          </span>

        </div>

      </header>


      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="main">

        {/* ===================================================
            HERO
        =================================================== */}

        <section className="hero">

          <div className="hero-icon">

            <Sparkles size={22} />

          </div>


          <h2>

            Your AI Weather

            <span>
              {" "}Intelligence
            </span>

          </h2>


          <p>
            Ask anything about weather, forecasts and historical trends.
          </p>


          {/* =================================================
              SEARCH
          ================================================= */}

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


          {/* =================================================
              QUICK QUESTIONS
          ================================================= */}

          <div className="quick-questions">

            <button
              onClick={() =>
                quickQuestion(
                  "What is the temperature in Mandya?"
                )
              }
            >

              <Thermometer size={16} />

              Current weather

            </button>


            <button
              onClick={() =>
                quickQuestion(
                  "What is the forecast for Mandya?"
                )
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


            <button
              onClick={() =>
                quickQuestion(
                  "Is there any danger of heavy rain or flooding in Mandya?"
                )
              }
            >

              <ShieldAlert size={16} />

              Weather Risk

            </button>

          </div>

        </section>


        {/* =====================================================
            LOADING
        ===================================================== */}

        {loading && (

          <div className="loading-card">

            <div className="loader"></div>

            <p>
              WeatherGPT is analyzing your question...
            </p>

          </div>

        )}


        {/* =====================================================
            SUCCESS RESPONSE
        ===================================================== */}

        {response && response.success && (

          <section className="result-section">


            {/* =================================================
                LOCATION
            ================================================= */}

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


            {/* =================================================
                CURRENT WEATHER
            ================================================= */}

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


            {/* =================================================
                WEATHER RISK ANALYSIS
            ================================================= */}

            {response.risk_analysis && (

              <div className="risk-section">


                {/* =============================================
                    RISK HEADER
                ============================================= */}

                <div className="risk-header">

                  <div className="risk-heading">

                    <div className="risk-title-icon">

                      <ShieldAlert size={21} />

                    </div>


                    <div>

                      <h3>
                        Weather Risk Analysis
                      </h3>

                      <p>
                        AI-assisted analysis of current and forecast
                        conditions
                      </p>

                    </div>

                  </div>


                  <div
                    className={`overall-risk-badge ${getRiskClass(
                      response.risk_analysis.overall_level
                    )}`}
                  >

                    <span>
                      Overall Risk
                    </span>

                    <strong>
                      {response.risk_analysis.overall_level}
                    </strong>

                  </div>

                </div>


                {/* =============================================
                    RISK INDICATORS
                ============================================= */}

                {response.risk_analysis.indicators && (

                  <div className="risk-indicators">


                    <div className="risk-indicator-card">

                      <CloudRain size={18} />

                      <span>
                        Rain Periods
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .rain_periods
                        }
                      </strong>

                    </div>


                    <div className="risk-indicator-card">

                      <CloudRain size={18} />

                      <span>
                        Heavy Rain
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .heavy_rain_periods
                        }
                      </strong>

                    </div>


                    <div className="risk-indicator-card">

                      <CloudLightning size={18} />

                      <span>
                        Thunderstorms
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .thunderstorm_periods
                        }
                      </strong>

                    </div>


                    <div className="risk-indicator-card">

                      <Wind size={18} />

                      <span>
                        High Wind
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .high_wind_periods
                        }
                      </strong>

                    </div>


                    <div className="risk-indicator-card">

                      <Droplets size={18} />

                      <span>
                        Max Rain Chance
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .maximum_rain_probability
                        }%
                      </strong>

                    </div>


                    <div className="risk-indicator-card">

                      <Waves size={18} />

                      <span>
                        Max Rain / 3h
                      </span>

                      <strong>
                        {
                          response.risk_analysis.indicators
                            .maximum_rain_amount_3h_mm
                        } mm
                      </strong>

                    </div>

                  </div>

                )}


                {/* =============================================
                    PRIORITY RISK
                ============================================= */}

                {response.risk_analysis.priority_risk && (

                  <div className="priority-risk">

                    <AlertTriangle size={16} />

                    <span>
                      Priority Risk:
                    </span>

                    <strong>
                      {formatRiskType(
                        response.risk_analysis.priority_risk
                      )}
                    </strong>

                  </div>

                )}


                {/* =============================================
                    DETECTED RISKS
                ============================================= */}

                {response.risk_analysis.risks?.length > 0 ? (

                  <div className="detected-risks">


                    <div className="risk-subtitle">

                      <AlertTriangle size={18} />

                      <h4>
                        Detected Risks
                      </h4>

                    </div>


                    <div className="risk-list">


                      {response.risk_analysis.risks.map(
                        (risk, index) => (

                          <div
                            className={`risk-card ${getRiskClass(
                              risk.level
                            )}`}
                            key={index}
                          >


                            {/* RISK TITLE */}

                            <div className="risk-card-top">

                              <div className="risk-card-title">


                                <div className="risk-card-icon">

                                  {getRiskIcon(
                                    risk.type
                                  )}

                                </div>


                                <div>

                                  <h4>
                                    {formatRiskType(
                                      risk.type
                                    )}
                                  </h4>

                                  <span>
                                    {risk.level} risk
                                  </span>

                                </div>

                              </div>


                              {risk.severity_score && (

                                <div className="severity-score">

                                  Score{" "}

                                  {risk.severity_score}

                                  /3

                                </div>

                              )}

                            </div>


                            {/* WHY */}

                            <div className="risk-reason">

                              <strong>
                                Why?
                              </strong>

                              <p>
                                {risk.reason}
                              </p>

                            </div>


                            {/* EVIDENCE */}

                            {risk.evidence && (

                              <div className="risk-evidence">

                                <strong>
                                  Evidence
                                </strong>


                                <div className="evidence-grid">

                                  {Object.entries(
                                    risk.evidence
                                  ).map(
                                    ([key, value]) => (

                                      <div
                                        className="evidence-item"
                                        key={key}
                                      >

                                        <span>
                                          {formatEvidenceKey(
                                            key
                                          )}
                                        </span>

                                        <strong>
                                          {formatEvidenceValue(
                                            key,
                                            value
                                          )}
                                        </strong>

                                      </div>

                                    )
                                  )}

                                </div>

                              </div>

                            )}


                            {/* SAFETY ADVICE */}

                            <div className="risk-advice">

                              <strong>
                                Safety Advice
                              </strong>

                              <p>
                                {risk.advice}
                              </p>

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                ) : (

                  <div className="no-risk-card">

                    <div>

                      <ShieldAlert size={21} />

                    </div>


                    <div>

                      <strong>
                        No significant weather risks detected
                      </strong>

                      <p>
                        The available current and forecast data
                        does not indicate a significant weather risk.
                      </p>

                    </div>

                  </div>

                )}

              </div>

            )}


            {/* =================================================
                FORECAST
            ================================================= */}

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


            {/* =================================================
                HISTORICAL WEATHER
            ================================================= */}

            {response.summary && (

              <div className="forecast-card">

                <div className="section-title">

                  <History size={19} />

                  <h3>
                    Historical Summary —{" "}
                    {response.summary.year}
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


            {/* =================================================
                AI ANSWER
            ================================================= */}

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


              <div className="ai-answer-content">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                >
                  {response.answer}
                </ReactMarkdown>

              </div>

            </div>

          </section>

        )}


        {/* =====================================================
            ERROR
        ===================================================== */}

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


      {/* =====================================================
          FOOTER
      ===================================================== */}

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