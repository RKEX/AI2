import requests
from datetime import datetime


def get_location():
    latitude = 22.7264
    longitude = 88.4753
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": f"{latitude},{longitude}",
        "key": "105ae62c16824b05955a777220824fdb",  # Your OpenCage API key
        "pretty": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            components = data['results'][0]['components']
            city = components.get('city', '')
            town = components.get('town', '')
            suburb = components.get('suburb', '')
            state = components.get('state', '')
            postcode = components.get('postcode', '')
            country = components.get('country', '')

            if not city:
                city = town or suburb

            if postcode != "700124":
                postcode = "700124"

            location = f"{city}, Kolkata {postcode}, {state}, {country}"
            return location
        else:
            print("Location details are not available.")
            return None
    else:
        print("Error retrieving location information.")
        return None


def format_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")
        return formatted_time
    except ValueError:
        return time_str


def get_weather():
    location = get_location()
    if location is None:
        print("Could not retrieve location. Exiting weather check.")
        return

    latitude = 22.7264
    longitude = 88.4753
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset,windspeed_10m_max,winddirection_10m_dominant",
        "timezone": "Asia/Kolkata"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get('current_weather', {})
        daily_weather = data.get('daily', {})

        # Modern weather-related icons (more stylized)
        temp_icon = "🌞"  # Sun
        max_temp_icon = "🔥"  # Fire
        min_temp_icon = "❄️"  # Snowflake
        rain_icon = "🌧️"  # Cloud with rain
        sunrise_icon = "🌅"  # Sunrise
        sunset_icon = "🌇"  # Sunset
        wind_icon = "🌬️"  # Wind
        wind_direction_icon = "🧭"  # Compass

        # Display current weather
        print(f"\nWeather Information for {location} (Today):")
        print(f"{temp_icon} Current Temperature: {current_weather.get('temperature', 'N/A')} °C")
        print(f"{max_temp_icon} Max Temperature: {daily_weather.get('temperature_2m_max', ['N/A'])[0]} °C")
        print(f"{min_temp_icon} Min Temperature: {daily_weather.get('temperature_2m_min', ['N/A'])[0]} °C")
        print(f"{rain_icon} Precipitation: {daily_weather.get('precipitation_sum', ['N/A'])[0]} mm")

        # Format and display Sunrise and Sunset times
        sunrise = format_time(daily_weather.get('sunrise', ['N/A'])[0])
        sunset = format_time(daily_weather.get('sunset', ['N/A'])[0])
        print(f"{sunrise_icon} Sunrise: {sunrise}")
        print(f"{sunset_icon} Sunset: {sunset}")

        # Display wind information
        print(f"{wind_icon} Wind Speed: {current_weather.get('windspeed', 'N/A')} km/h")
        print(f"{wind_direction_icon} Wind Direction: {current_weather.get('winddirection', 'N/A')} degrees")

        # Display the weather forecast for the next 7 days
        print("\nForecast for the next 7 days:")
        for i in range(7):  # Loop through the next 7 days (including today)
            print(f"\nDay {i + 1}:")
            print(f"{max_temp_icon} Max Temperature: {daily_weather.get('temperature_2m_max', ['N/A'])[i]} °C")
            print(f"{min_temp_icon} Min Temperature: {daily_weather.get('temperature_2m_min', ['N/A'])[i]} °C")
            print(f"{rain_icon} Precipitation: {daily_weather.get('precipitation_sum', ['N/A'])[i]} mm")

            # Format and display Sunrise and Sunset times for each day
            sunrise = format_time(daily_weather.get('sunrise', ['N/A'])[i])
            sunset = format_time(daily_weather.get('sunset', ['N/A'])[i])
            print(f"{sunrise_icon} Sunrise: {sunrise}")
            print(f"{sunset_icon} Sunset: {sunset}")

            # Display wind information for the next days
            print(f"{wind_icon} Wind Speed: {daily_weather.get('windspeed_10m_max', ['N/A'])[i]} km/h")
            print(
                f"{wind_direction_icon} Wind Direction: {daily_weather.get('winddirection_10m_dominant', ['N/A'])[i]} degrees")

    else:
        print("Unable to retrieve the weather information at the moment.")


def main():
    while True:
        command = input("Enter 'weather' to get the current weather information or 'exit' to quit: ").strip().lower()
        if command == 'weather':
            get_weather()
        elif command == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid command. Please enter 'weather' to retrieve weather information or 'exit' to quit.")


if __name__ == "__main__":
    main()
