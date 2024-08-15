from main import *

def get_weather_data(city):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response=requests.get(url)
    return response.json()

# Function to calculate the daily summaries
def calculate_daily_summary(daily_data):
    df=pd.DataFrame(daily_data)
    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    dominant_condition = Counter(df['weather_type']).most_common(1)[0][0]
    avg_humidity = df['humidity'].mean()
    avg_wind_speed = df['wind_speed'].mean()
    return {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "avg_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_condition": dominant_condition,
        "avg_humidity": avg_humidity,
        "avg_wind_speed": avg_wind_speed
    }

# Function to get the data through API and store it in the database
def background_data_fetch():
    # time.sleep(100000)
    # count=0
    daily_data={}
    while True:
        for city in cities:
            daily_data[city]=[]
        updates_collection={"city":[], "weather_type":[], "temp":[], "feels_like":[], "time_of_data":[], "humidity":[], "wind_speed":[]}
        for city in cities:
            weather_data=get_weather_data(city)
            weather_type = weather_data['weather'][0]['main']
            temp=(weather_data['main']['temp'])
            feels_like=(weather_data['main']['feels_like'])
            time_of_data=weather_data['dt']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            update={"city":city, "weather_type":weather_type, "temp":temp, "feels_like":feels_like, "time_of_data":time_of_data, "humidity":humidity, "wind_speed":wind_speed}
            daily_data[city].append(update)
            updates_collection["city"].append(city)
            updates_collection["weather_type"].append(weather_type)
            updates_collection["temp"].append(temp)
            updates_collection["feels_like"].append(feels_like)
            updates_collection["time_of_data"].append(time_of_data)
            updates_collection["humidity"].append(humidity)
            updates_collection["wind_speed"].append(wind_speed)
        mongo.db.updates.insert_one(updates_collection)
        # count+=1
        if datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 59:
        # if(count%3==0):
            for city in cities:
                daily_summary = calculate_daily_summary(daily_data[city])
                if(city=="Delhi"):
                    mongo.db.daily_summaries_delhi.insert_one(daily_summary)
                elif(city=="Mumbai"):
                    mongo.db.daily_summaries_mumbai.insert_one(daily_summary)
                elif(city=="Chennai"):
                    mongo.db.daily_summaries_chennai.insert_one(daily_summary)
                elif(city=="Bangalore"):
                    mongo.db.daily_summaries_bangalore.insert_one(daily_summary)
                elif(city=="Kolkata"):
                    mongo.db.daily_summaries_kolkata.insert_one(daily_summary)
                elif(city=="Hyderabad"):
                    mongo.db.daily_summaries_hyderabad.insert_one(daily_summary)
        daily_data = {}
        # time.sleep(20)
        time.sleep(300)


