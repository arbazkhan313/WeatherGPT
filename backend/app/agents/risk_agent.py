class RiskAgent:

    def analyze_risk(self, current_weather, forecast_data):

        risks = []

        # =========================================================
        # CURRENT WEATHER
        # =========================================================

        temperature = current_weather.get("temperature", 0)
        feels_like = current_weather.get("feels_like", temperature)
        humidity = current_weather.get("humidity", 0)
        wind_speed = current_weather.get("wind_speed", 0)

        # =========================================================
        # FORECAST DATA
        # =========================================================

        forecast = forecast_data.get("forecast", [])

        rain_periods = 0
        heavy_rain_periods = 0
        thunderstorm_periods = 0
        high_wind_periods = 0

        max_rain_probability = 0
        max_rain_amount = 0
        max_wind_speed = 0
        max_wind_gust = 0

        # =========================================================
        # ANALYZE FORECAST
        # =========================================================

        for item in forecast:

            weather_main = item.get(
                "weather_main",
                ""
            ).lower()

            weather_description = item.get(
                "weather",
                ""
            ).lower()

            rain_amount = item.get(
                "rain_3h_mm",
                0
            ) or 0

            rain_probability = item.get(
                "precipitation_probability",
                0
            ) or 0

            wind_speed_forecast = item.get(
                "wind_speed",
                0
            ) or 0

            wind_gust = item.get(
                "wind_gust",
                0
            ) or 0

            # -----------------------------------------------------
            # RAIN
            # -----------------------------------------------------

            if (
                weather_main in ["rain", "thunderstorm"]
                or "rain" in weather_description
                or "drizzle" in weather_description
            ):
                rain_periods += 1

            # -----------------------------------------------------
            # HEAVY RAIN
            # -----------------------------------------------------

            if (
                rain_amount >= 10
                or "heavy rain" in weather_description
            ):
                heavy_rain_periods += 1

            # -----------------------------------------------------
            # THUNDERSTORM
            # -----------------------------------------------------

            if (
                weather_main == "thunderstorm"
                or "thunderstorm" in weather_description
            ):
                thunderstorm_periods += 1

            # -----------------------------------------------------
            # HIGH WIND
            # -----------------------------------------------------

            if (
                wind_speed_forecast >= 15
                or wind_gust >= 20
            ):
                high_wind_periods += 1

            # -----------------------------------------------------
            # MAXIMUM VALUES
            # -----------------------------------------------------

            max_rain_probability = max(
                max_rain_probability,
                rain_probability
            )

            max_rain_amount = max(
                max_rain_amount,
                rain_amount
            )

            max_wind_speed = max(
                max_wind_speed,
                wind_speed_forecast
            )

            max_wind_gust = max(
                max_wind_gust,
                wind_gust
            )

        # =========================================================
        # 1. HEAT RISK
        # =========================================================

        if temperature >= 40:

            risks.append({
                "type": "heat",
                "level": "high",
                "severity_score": 3,
                "reason": (
                    f"Current temperature is {temperature}°C "
                    f"with a feels-like temperature of {feels_like}°C."
                ),
                "evidence": {
                    "temperature": temperature,
                    "feels_like": feels_like,
                    "humidity": humidity
                },
                "advice": (
                    "Avoid prolonged outdoor exposure, stay hydrated, "
                    "and avoid strenuous activity during peak heat."
                )
            })

        elif temperature >= 35:

            risks.append({
                "type": "heat",
                "level": "moderate",
                "severity_score": 2,
                "reason": (
                    f"Current temperature is {temperature}°C "
                    f"with a feels-like temperature of {feels_like}°C."
                ),
                "evidence": {
                    "temperature": temperature,
                    "feels_like": feels_like,
                    "humidity": humidity
                },
                "advice": (
                    "Stay hydrated and limit strenuous outdoor activity "
                    "during the hottest part of the day."
                )
            })

        # =========================================================
        # 2. CURRENT WIND RISK
        # =========================================================

        if wind_speed >= 15:

            risks.append({
                "type": "wind",
                "level": "high",
                "severity_score": 3,
                "reason": (
                    f"Current wind speed is {wind_speed} m/s."
                ),
                "evidence": {
                    "current_wind_speed": wind_speed
                },
                "advice": (
                    "Avoid exposed areas and secure loose outdoor objects."
                )
            })

        elif wind_speed >= 10:

            risks.append({
                "type": "wind",
                "level": "moderate",
                "severity_score": 2,
                "reason": (
                    f"Current wind speed is {wind_speed} m/s."
                ),
                "evidence": {
                    "current_wind_speed": wind_speed
                },
                "advice": (
                    "Use caution in exposed or open areas."
                )
            })

        # =========================================================
        # 3. HEAVY RAIN RISK
        # =========================================================

        if heavy_rain_periods >= 3 or max_rain_amount >= 25:

            risks.append({
                "type": "heavy_rain",
                "level": "high",
                "severity_score": 3,
                "reason": (
                    f"Heavy-rain indicators appear in "
                    f"{heavy_rain_periods} forecast period(s). "
                    f"Maximum forecast rainfall is "
                    f"{max_rain_amount} mm over 3 hours."
                ),
                "evidence": {
                    "heavy_rain_periods": heavy_rain_periods,
                    "maximum_rain_amount_3h_mm": max_rain_amount,
                    "maximum_rain_probability": max_rain_probability
                },
                "advice": (
                    "Avoid unnecessary travel during intense rainfall. "
                    "Stay away from waterlogged and low-lying areas."
                )
            })

        elif heavy_rain_periods >= 1 or max_rain_amount >= 10:

            risks.append({
                "type": "heavy_rain",
                "level": "moderate",
                "severity_score": 2,
                "reason": (
                    f"Heavy-rain indicators appear in "
                    f"{heavy_rain_periods} forecast period(s). "
                    f"Maximum forecast rainfall is "
                    f"{max_rain_amount} mm over 3 hours."
                ),
                "evidence": {
                    "heavy_rain_periods": heavy_rain_periods,
                    "maximum_rain_amount_3h_mm": max_rain_amount,
                    "maximum_rain_probability": max_rain_probability
                },
                "advice": (
                    "Carry rain protection and use caution around "
                    "waterlogged or low-lying areas."
                )
            })

        # =========================================================
        # 4. GENERAL RAIN RISK
        # =========================================================

        elif rain_periods >= 1:

            risks.append({
                "type": "rain",
                "level": "moderate",
                "severity_score": 2,
                "reason": (
                    f"Rain is present in {rain_periods} "
                    f"forecast period(s)."
                ),
                "evidence": {
                    "rain_periods": rain_periods,
                    "maximum_rain_probability": max_rain_probability,
                    "maximum_rain_amount_3h_mm": max_rain_amount
                },
                "advice": (
                    "Carry an umbrella or rain protection "
                    "if you are going outdoors."
                )
            })

        # =========================================================
        # 5. HIGH PRECIPITATION PROBABILITY
        # =========================================================

        if max_rain_probability >= 80:

            risks.append({
                "type": "precipitation_probability",
                "level": "moderate",
                "severity_score": 2,
                "reason": (
                    f"Maximum forecast precipitation probability "
                    f"is {max_rain_probability}%."
                ),
                "evidence": {
                    "maximum_probability": max_rain_probability
                },
                "advice": (
                    "Plan outdoor activities with rain as a possibility "
                    "and keep rain protection available."
                )
            })

        # =========================================================
        # 6. THUNDERSTORM RISK
        # =========================================================

        if thunderstorm_periods >= 1:

            risks.append({
                "type": "thunderstorm",
                "level": "high",
                "severity_score": 3,
                "reason": (
                    f"Thunderstorm conditions appear in "
                    f"{thunderstorm_periods} forecast period(s)."
                ),
                "evidence": {
                    "thunderstorm_periods": thunderstorm_periods
                },
                "advice": (
                    "Avoid open areas during thunderstorms and seek "
                    "shelter indoors when thunder or lightning is present."
                )
            })

        # =========================================================
        # 7. FORECAST WIND RISK
        # =========================================================

        if high_wind_periods >= 1:

            if max_wind_gust >= 25 or max_wind_speed >= 18:
                wind_level = "high"
                severity_score = 3
            else:
                wind_level = "moderate"
                severity_score = 2

            risks.append({
                "type": "forecast_wind",
                "level": wind_level,
                "severity_score": severity_score,
                "reason": (
                    f"Strong-wind indicators appear in "
                    f"{high_wind_periods} forecast period(s). "
                    f"Maximum forecast wind speed is "
                    f"{max_wind_speed} m/s and maximum gust is "
                    f"{max_wind_gust} m/s."
                ),
                "evidence": {
                    "high_wind_periods": high_wind_periods,
                    "maximum_wind_speed": max_wind_speed,
                    "maximum_wind_gust": max_wind_gust
                },
                "advice": (
                    "Secure loose objects and avoid exposed areas "
                    "during strong winds."
                )
            })

        # =========================================================
        # 8. FLOODING INDICATOR
        # =========================================================

        flood_indicator = False

        if (
            heavy_rain_periods >= 2
            and max_rain_amount >= 20
        ):
            flood_indicator = True

        if (
            max_rain_amount >= 30
            and max_rain_probability >= 70
        ):
            flood_indicator = True

        if flood_indicator:

            risks.append({
                "type": "flood",
                "level": "high",
                "severity_score": 3,
                "reason": (
                    "The forecast contains multiple heavy-rain "
                    "indicators with substantial rainfall."
                ),
                "evidence": {
                    "heavy_rain_periods": heavy_rain_periods,
                    "maximum_rain_amount_3h_mm": max_rain_amount,
                    "maximum_rain_probability": max_rain_probability
                },
                "advice": (
                    "Avoid low-lying and waterlogged areas. "
                    "Do not attempt to cross flooded roads "
                    "or flowing water."
                )
            })

        # =========================================================
        # 9. OVERALL RISK
        # =========================================================

        severity_scores = [
            risk.get("severity_score", 1)
            for risk in risks
        ]

        if not severity_scores:

            overall_level = "low"
            overall_score = 0

        else:

            overall_score = max(severity_scores)

            if overall_score >= 3:
                overall_level = "high"

            elif overall_score >= 2:
                overall_level = "moderate"

            else:
                overall_level = "low"

        # =========================================================
        # 10. PRIORITY RISK
        # =========================================================

        priority_risk = None

        if risks:

            priority_risk = max(
                risks,
                key=lambda risk: risk.get(
                    "severity_score",
                    0
                )
            )

        # =========================================================
        # RETURN RESULT
        # =========================================================

        return {

            "overall_level": overall_level,

            "overall_score": overall_score,

            "priority_risk": (
                priority_risk["type"]
                if priority_risk
                else None
            ),

            "indicators": {

                "rain_periods": rain_periods,

                "heavy_rain_periods": heavy_rain_periods,

                "thunderstorm_periods": thunderstorm_periods,

                "high_wind_periods": high_wind_periods,

                "maximum_rain_probability": max_rain_probability,

                "maximum_rain_amount_3h_mm": max_rain_amount,

                "maximum_wind_speed": max_wind_speed,

                "maximum_wind_gust": max_wind_gust
            },

            "risks": risks
        }
