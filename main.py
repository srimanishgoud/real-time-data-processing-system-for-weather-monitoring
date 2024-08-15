import datetime
import requests
from collections import Counter
import time
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

API_KEY="ce482827e7cb589044b70c44ec0bdb24"
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myWeatherDatabase"
mongo = PyMongo(app)


cities=["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
different_weather_types=["Thunderstorm", "Drizzle", "Rain", "Snow", "Clear", "Clouds", "Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"]


def kelvin_to_celsius(temp):
    return temp - 273.15
def kelvin_to_farhenheit(temp):
    return (temp - 273.15) * 9/5 + 32

temp_conversion={
    'Kelvin': lambda x: x,
    'Celsius': kelvin_to_celsius,
    'Fahrenheit': kelvin_to_farhenheit
}

temp_conversion_to_Kelvin={
    'Kelvin': lambda x: x,
    'Celsius': lambda x: x + 273.15,
    'Fahrenheit': lambda x: (x - 32) * 5/9 + 273.15
}

temp_symbol={
    'Kelvin': 'K',
    'Celsius': '°C',
    'Fahrenheit': '°F'
}



# database contents
# alerts - to store the all the alerts set by the user
# alerts_store - to store the triggered alerts
# daily_summaries_city - daily summaries of the respective city
# updates - to store the combined data for all the cities for every 5 minutes