# 🌍 World Explorer

World Explorer is a desktop application built with Python and Tkinter that lets users explore countries around the world. It displays key information, current weather, and top news headlines for each country—all in a clean, interactive interface.

---

## ✨ Features

- 🗺 Browse countries with a searchable list
- 🏛 View capital, region, population, language, and currency
- 🌦 Get real-time weather data for each capital city
- 🗞 See the latest top news headlines per country
- 🖼 Display each country’s flag

---

## 📦 Installation

### 🔧 Requirements (for running from source)

- Python 3.8+
- Required libraries:
  ```bash
  pip install requests pandas pillow tkinter Image ImageTK BytesIO date timedelta  webbrowser
  ```

### 🚀 Run the App

```bash
python world_explorer.py
```


## 🔑 API Keys

This app uses:

- [WeatherAPI](https://www.weatherapi.com/) for weather data
- [NewsAPI](https://newsapi.org/) for news headlines

To use the app, insert your API keys in the appropriate functions:

```python
get_current_weather()
get_country_news()
```

---


---

## 🧠 Credits

Built with ❤️ by Abdelaziz using:

- Python + Tkinter
- Pillow for image handling
- Requests for API calls
- Pandas for data manipulation

---

## 📜 License

This project is open-source and free to use for educational and personal purposes.
