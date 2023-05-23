from flask import Flask, jsonify, request, render_template
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

app = Flask(__name__)

def get_weather_forecast(city):
    api_key = "ccb00775b51fc52909b93c4eb24522c9"  # Replace with your OpenWeatherMap API key
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city + ",IN",
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if weather_data.get("cod") == "404":
        return {"error": "City not found."}
    else:
        forecast_items = weather_data["list"]
        forecast = []

        for item in forecast_items:
            timestamp = item["dt"]
            temperature = item["main"]["temp"]
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

            forecast.append({"date": date, "temperature": temperature})

        return forecast

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather-forecast", methods=["GET"])
def weather_forecast():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is missing."}), 400

    forecast = get_weather_forecast(city)

    if "error" in forecast:
        return jsonify(forecast), 404

    dates = ["20-05-2023", "21-05-2023", "22-05-2023", "23-05-2023"]
    temperatures = []

    for data in forecast[:4]:
        temperatures.append(data["temperature"])

    # Create the graph
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    plt.plot(dates, temperatures, marker="o")
    plt.title(f"Estimated Weather Forecast for {city}, at this time")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    # Save the graph to a file
    graph_filename = f"static/{city}_graph.png"  # Specify the path where you want to save the graph image
    plt.savefig(graph_filename)

    # Return the graph image file path
    return jsonify({"graph_path": graph_filename})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
