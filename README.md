# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates

## Steps to use the App
After downloading or cloning the repository navigate to the project folder. After that,
1. Install and create a virtual env using the command `virtualenv flask`
> **_Note_**: Make sure that the python version is greater than 3.10
2. Activate the virtual environment using 
> For mac/linux: `source flask/bin/activate`\
> For windows: `.\flask\Scripts\activate`\
> **_Note_**: To deactivate the environment use the command `deactivate`
3. Install the required packages from the `requirements.txt` file using the command `pip install -r requirements.txt`.
4. `main.py` contains the database information and API keys.
> Make sure to replace the API_KEY variable with your own api key from OpenWeatherMap API.
> I am using MongoDB database, we can have a look into to the data using MongoDB Compass.
> We can download MongoDB community server from https://www.mongodb.com/try/download/community.
5. Run the app using `streamlit run app.py`\

## Details about the App
1. I have utilized streamlit to build the UI.
2. We can access `Weather data`, `Daily Weather Summaries`, and `Alert` details using the side panel in the application through navigating.
3. Here we are running background_data_fetch: to fetch the data continuously through API, check_alerts:to check for the alerts, continuously irrespective of the user interaction with the application using different processes for those functions.
4. `Weather Data`/`Know the Weather`: This page gives the weather conditions at that time upon selecting the city and the temperature units. 
> It displays city, weather type, temperature, Feels Like tempertaure, Humidity, wind speed, and Unix timespamp of the data.
5.  `Display daily summary`: Upon selecting the city, temperature units and the time frame of which the data should be displayed, the data is then projected and also the graphical representation of the data is also displayed below it.
> It displays date, Average temperatire, Maximum temperature, Minimum temperature, Dominant Weather Condition of the day, Average Humidity and Average Wind speed. I chose to not display max and min humidity and wind speed of the day because its not that important to display that data also it might get clumsy in the app UI anyway when we can get an idea of it from its average value.
> Q: `Dominant Weather Condition` \
> Ans: Dominant weather condition for the day is the weather condition that is observed most number of time in that particular day.
6. `Alerts`: Alerts page contains all the functionalities that a user can use to manage alerts based on weather conditions. 
> `Set Alerts` is used to create a new alert. \
> `All Alerts` displays all the active alerts. \
> `Delete Alerts` is used to delete a particular alert using its data. \
> `Past Triggered Alerts` displays all the previously triggered alerts. It displays the date, time and the alert message of when it was triggered.
7. `Database and its collections`: MondoDB database
> myWeatherDatabase - database name \
> alerts - to store the all the alerts set by the user \
> alerts_store - to store the triggered alerts \
> daily_summaries_city - daily summaries of the respective city \
> updates - to store the combined data for all the cities that is generated for every 5 minutes.

## Files description
`main.py` : This file contains all the things needed to start the app, like, database, API_KEY. Also, it contains helper functions needed for temperture unit conversion. \
`data.py`: This files contains the functions for data fetching through the API and calculating daily summaries. \
`requirements.txt`: This file contains all the libraries needed to run the app. Install them before running the application. \
`app.py`: This file contains the functions to run the app and control user interactions with the app.

### Generating sample data
We can generate the sample data to fill the database, just to test the app, by simply setting the sleep time to 5 seconds and filling the daily summary for each city after 3 rounds of 5 sec. For clarity visit the data.py file and look at the commented code in background_data_fetch function. This data is not the actual representation of what actual data might look like but its keeps us get started.
