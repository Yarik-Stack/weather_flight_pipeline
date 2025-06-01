# weather_flights_pipeline

A modular Python data pipeline that gathers and stores information about cities, current weather, nearby airports, and recent arriving flights. The data is parsed from Wikipedia and enriched using **OpenWeatherMap** and **AeroDataBox** APIs, then stored in a **MySQL** database.

---

## Features

- City parsing from Wikipedia (name, country, coordinates, population)  
- Weather fetching via OpenWeatherMap API  
- Airport & flight info via AeroDataBox API  
- Data storage using SQLAlchemy & MySQL  
- Modular design (functions split into logical files)  
- `.env.example` included for easy configuration  
- Ready for local run, cloud deployment, or GitHub integration  

---

## Project Structure

```
weather_flights_pipeline/
│
├── cities_parser.py         # Parsing cities and their data
├── weather.py               # Fetching weather data
├── flights.py               # Fetching airport and flight data
├── db_connection.py         # Connecting to the database
├── utils.py                 # Utility functions (env loader, merging, etc.)
├── main.py                  # Entry point to run the full pipeline
│
├── sql_table_creation.sql   # SQL script to create necessary tables
├── .env.example             # Example config for environment variables
├── requirements.txt         # Project dependencies
└── .gitignore               # Git ignored files and folders
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Yarik-Stack/weather_flights_pipeline.git
cd weather_flights_pipeline
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# OR
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Then fill in your:

- MySQL credentials  
- OpenWeatherMap API key  
- AeroDataBox API key  

---

## Running the Pipeline

```bash
python main.py
```

All data will be pulled, processed, and saved to your MySQL database.

---

## Environment Variables

Your `.env` file should include:

```env
DB_NAME=your_db_name
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_PORT=3306
WEATHER_API_KEY=your_openweather_key
AERODATABOX_API_KEY=your_aerodatabox_key
```

> Keep your `.env` file secret — it’s ignored by Git using `.gitignore`.

---

## Database Schema

Use `sql_table_creation.sql` to create the required tables in your MySQL database.

---

## License

This project is open-source and available under the **MIT License**.
