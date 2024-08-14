import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import datetime

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky", "Summary"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)
        dates = [datetime.strptime(data["dt_txt"], '%Y-%m-%d %H:%M:%S') for data in filtered_data]

        if option == "Temperature":
            temperatures = [data["main"]["temp"] for data in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [data["weather"][0]["main"] for data in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115, caption=sky_conditions)

        elif option == "Summary":
            temps = [data["main"]["temp"] for data in filtered_data]
            humidity = [data["main"]["humidity"] for data in filtered_data]
            wind_speed = [data["wind"]["speed"] for data in filtered_data]
            descriptions = [data["weather"][0]["description"] for data in filtered_data]

            min_temp = min(temps)
            max_temp = max(temps)
            avg_humidity = sum(humidity) / len(humidity)
            avg_wind_speed = sum(wind_speed) / len(wind_speed)

            st.write(f"**Min Temperature:** {min_temp:.1f}°C")
            st.write(f"**Max Temperature:** {max_temp:.1f}°C")
            st.write(f"**Average Humidity:** {avg_humidity:.1f}%")
            st.write(f"**Average Wind Speed:** {avg_wind_speed:.1f} m/s")
            st.write("**Descriptions:**")
            for date, desc in zip(dates, descriptions):
                st.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - {desc.capitalize()}")

    except KeyError:
        st.error("Could not retrieve data for the specified place. Please check the location and try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
