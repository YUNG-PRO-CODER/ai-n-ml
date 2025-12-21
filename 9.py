import requests

API_KEY = "b95f16e6904b54c27687ad31cf6cd63d"

country = input("Enter country code (e.g. IN, US): ").strip().upper()
state = input("Enter state name: ").strip()
city = input("Enter city name: ").strip()

geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={API_KEY}"

geo_response = requests.get(geo_url)
geo_data = geo_response.json()

print("Geocoding response:", geo_data)


if not geo_data:
    print(f'❌ "{city}" is not located in "{state}" or country "{country}".')
else:
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]
    weather_url = (f"https://api.openweathermap.org/data/2.5/weather?"f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    description = weather_data["weather"][0]["description"]

    print("\n✅ Location Verified!")
    print("City:", city)
    print("State:", state)
    print("Country:", country)
    print("Temperature:", temp, "°C")
    print("Humidity:", humidity, "%")
    print("Weather:", description)
