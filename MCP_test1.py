from flask import Flask, request, jsonify

# Create a Flask web server
app = Flask("WeatherService")

@app.route('/weather', methods=['GET'])
def get_weather():
    """Get the current weather for a specific city."""
    city = request.args.get('city', 'Unknown')
    # In a real app, you'd call a weather API here
    return jsonify({
        "city": city,
        "weather": f"The weather in {city} is sunny and 25°C.",
        "temperature": 25,
        "condition": "sunny"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "WeatherService"})

if __name__ == "__main__":
    print("Starting WeatherService on http://localhost:5000")
    print("Try: http://localhost:5000/weather?city=London")
    app.run(host='0.0.0.0', port=5000, debug=True)
