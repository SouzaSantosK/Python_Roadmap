# app.py
from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import WeatherModel

app = Flask(__name__)
weather_model = WeatherModel()


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    if request.method == 'POST' or request.args.get('city'):
        city = request.form.get('city') or request.args.get('city')
        
        data, source = weather_model.get_weather(city)

        if "error" in source:
            error_message = data.get('error')
        else:
            current = data['currentConditions']
            
            days_forecast = data['days'][:5]

            filtered_days_forecast = []

            for day in days_forecast:
                day_hours = [h for h in day['hours'] if 6 <= int(h['datetime'][:2]) <= 18]
                night_hours = [h for h in day['hours'] if int(h['datetime'][:2]) > 18 or int(h['datetime'][:2]) < 6]

                day_data = {
                    'datetime': day['datetime'],
                    'temp_day': round(sum(h['temp'] for h in day_hours) / len(day_hours)),
                    'icon_day': weather_model.get_google_icon(day_hours[6]['icon']),
                    'temp_night': round(sum(h['temp'] for h in night_hours) / len
                    (night_hours)),
                    'icon_night': weather_model.get_google_icon(night_hours[2]['icon']),
                    'humidity': day['humidity'],
                    'precip': day['precip'],
                    'uvindex': day['uvindex'],
                    'windspeed': day['windspeed']
                }

                filtered_days_forecast.append(day_data)



            weather_data = {
                "city": data['resolvedAddress'],
                "current": {
                    "temp": round(current['temp']),
                    "feelslike": round(current['feelslike']),
                    "high": round(days_forecast[0]['tempmax']),
                    "low": round(days_forecast[0]['tempmin']),
                    "condition": current['conditions'],
                    "humidity": current['humidity'],
                    "uv": current['uvindex'],
                    'dew': current['dew'],
                    'uvvalue': current['uvindex'],
                    'uvindex': weather_model.get_uv_index(current['uvindex']),
                    'windspeed': current['windspeed'],
                    "winddesc": weather_model.get_wind_description(current['windspeed']),"winddirection": weather_model.get_wind_direction(current['windspeed']),
                    "icon": weather_model.get_google_icon(current['icon']),
                },
                "forecast": filtered_days_forecast,
                "source": source
            }

    return render_template('base.html', weather=weather_data, error=error_message)


@app.route("/weather/<city>", methods=["GET"])
@limiter.limit("10 per minute")
def get_weather(city):
    data, source = weather_model.get_weather(city)

    if "error" in source:
        status_code = 404 if source == "error_city" else 500
        if source == "error_auth":
            status_code = 401

        return jsonify(data), status_code

    current = data.get("currentConditions", {})

    return jsonify(current)


@app.errorhandler(429)
def ratelimit_handler(e):
    return (
        jsonify(
            {
                "error": "Access limit exceeded.",
                "message": str(e.description),
            }
        ),
        429,
    )


if __name__ == "__main__":
    app.run(debug=True)
