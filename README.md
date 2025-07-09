# 🌍 World Explorer

World Explorer is a desktop application built with Python and Tkinter that lets users explore countries around the world. It displays key information, current weather, and top news headlines for each country—all in a clean, interactive interface.

---

## ✨ Features

- 🗺 Browse countries with a searchable list
- 🏛 View capital, region, population, language, and currency
- 🌦 Get real-time weather data for each capital city
- 🗞 See the latest top news headlines per country
- 🖼 Display each country’s flag
- 📦 Packaged as a standalone `.exe` for Windows

---

## 📦 Installation

### 🔧 Requirements (for running from source)

- Python 3.8+
- Required libraries:
  ```bash
  pip install requests pandas pillow
  ```

### 🚀 Run the App

```bash
python world_explorer.py
```

### 🪄 Build the Executable (Optional)

To create a fast-launching `.exe`:

```bash
pyinstaller --clean --windowed --icon=icon.ico --add-data "country.csv;." world_explorer.py
```

> Make sure `country.csv` and `icon.ico` are in the same directory as your script.

---

## 🔑 API Keys

This app uses:

- [WeatherAPI](https://www.weatherapi.com/) for weather data
- [NewsAPI](https://newsapi.org/) for news headlines

To use the app, insert your API keys in the appropriate functions:

```python
weather_api_key = "YOUR_WEATHER_API_KEY"
news_api_key = "YOUR_NEWS_API_KEY"
```

---

## 📁 Project Structure

```
world_explorer/
├── world_explorer.py       # Main application script
├── country.csv             # Country data (auto-generated if missing)
├── icon.ico                # App icon
├── README.md               # This file
└── dist/                   # Output folder after building the .exe
```

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