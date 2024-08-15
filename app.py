from main import *
from data import *
from multiprocessing import Process

def home():
    st.title('Weather App')
    with st.form(key='my_form'):
        city = st.selectbox("Select City", cities)
        temp_type=st.selectbox('Select temperature type', ['Kelvin', 'Celsius', 'Fahrenheit'])
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        last_record = list(mongo.db.updates.find().sort("_id", -1).limit(1))[0]
        # get the subscriptable record from the above last_record cursor object
        # print("last_record: ", last_record)
        req_index=-1
        for i in range(len(last_record["city"])):
            if last_record['city'][i] == city:
                req_index=i
                break
        if req_index==-1:
            st.error("City not found")
        else:
            weather_type = last_record["weather_type"][req_index]
            print("weather type: ",weather_type)
            temp = str(temp_conversion[temp_type](last_record["temp"][req_index]))+" "+temp_symbol[temp_type]
            feels_like = str(temp_conversion[temp_type](last_record["feels_like"][req_index]))+" "+temp_symbol[temp_type]
            time_of_data = last_record["time_of_data"][req_index]
            humidity = str(last_record["humidity"][req_index])+ " %"
            wind_speed = str(last_record["wind_speed"][req_index])+" m/s"

            d = {"City ":[city], "Weather Type ":[weather_type], "Temperature ":[temp], "Feels Like ":[feels_like], "Humidity ": [humidity], "Wind Speed ": [wind_speed] ,"Time of Data ":[time_of_data]}
            d = pd.DataFrame(d).reset_index(drop=True)
            st.table(d)

        # weather_data=get_weather_data(city)
        # weather_type = weather_data['weather'][0]['main']
        # temp=str(temp_conversion[temp_type](weather_data['main']['temp']))+" "+temp_symbol[temp_type]
        # feels_like=str(temp_conversion[temp_type](weather_data['main']['feels_like']))+" "+temp_symbol[temp_type]
        # time_of_data=weather_data['dt']
        # d={"City ":[city], "Weather Type ":[weather_type], "Temperature ":[temp], "Feels Like ":[feels_like], "Time of Data ":[time_of_data]}
        # d=pd.DataFrame(d).reset_index(drop=True)
        # st.table(d)

def check_alerts():
    print("Entered check alerts")
    while True:
        alerts=mongo.db.alerts.find()
        for alert in alerts:
            city=alert["city"]
            temp=alert["temp"]
            weather_type=alert["weather_type"]
            while True:
                last_two_records = list(mongo.db.updates.find().sort("_id", -1).limit(2))
                last_record=last_two_records[0]
                second_last_record=last_two_records[1]
                req_index=-1
                for i in range(len(last_record["city"])):
                    if last_record["city"][i] == city:
                        req_index=i
                        break
                req_index2=-1   
                for i in range(len(second_last_record["city"])):
                    if second_last_record["city"][i] == city:
                        req_index2=i
                        break
                alert_message=""
                if(temp and weather_type):
                    if((last_record["temp"][req_index]>float(temp) and second_last_record["temp"][req_index2]>float(temp)) or (last_record["weather_type"][req_index].upper()==weather_type.upper() and second_last_record["weather_type"][req_index2].upper()==weather_type.upper())):
                        alert_message=(f"Alert: temperature and weather type condition met for {city}, {temp} K/{kelvin_to_celsius(temp)} °C/{kelvin_to_farhenheit(temp)} °F and {weather_type}")
                elif(temp):
                    if(last_record["temp"][req_index]>float(temp) and second_last_record["temp"][req_index2]>float(temp)):
                        alert_message=(f"Alert: temperature condition met for {city} and {temp} K/{kelvin_to_celsius(temp)} °C/{kelvin_to_farhenheit(temp)} °F")
                elif(weather_type):
                    if(last_record["weather_type"][req_index].upper()==weather_type.upper() and second_last_record["weather_type"][req_index2].upper()==weather_type.upper()):
                        alert_message=(f"Alert weather type condition met for {city} and {weather_type}")
                if(alert_message):
                    mongo.db.alerts_store.insert_one({"date":datetime.datetime.now().strftime("%Y-%m-%d"), "time":datetime.datetime.now().strftime("%H:%M:%S"), "Alert":alert_message})
                break
        time.sleep(360)


def alerts():
    st.title("Set Alerts")
    with st.form("alert_form"):
        city=st.selectbox("Select city", cities)
        temp_type=st.selectbox('Select temperature units in which you wish to set alert', ['Kelvin', 'Celsius', 'Fahrenheit'])
        temp=st.text_input("Enter the temperature (numerics) above which you want to set alert")
        weather_type=st.selectbox("Select weather type for alert", different_weather_types, index=None, placeholder="Select")
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        # print("temp and weather_type: ", temp, weather_type)
        if not temp and not weather_type:
            st.error("Please select atleast one condition to set alert")
            return
        # record = mongo.db.alerts.find_one({"city": city})
        # if not record:


        if(temp and weather_type):
            alert={"city": city, "temp": temp_conversion_to_Kelvin[temp_type](float(temp)), "weather_type":weather_type}
        elif(temp):
            alert={"city": city, "temp": temp_conversion_to_Kelvin[temp_type](float(temp)), "weather_type":None}
        elif(weather_type):
            alert={"city": city, "weather_type":weather_type, "temp":None}
        record=mongo.db.alerts.find_one(alert)
        if not record:
            mongo.db.alerts.insert_one(alert)
            st.success("Alert set successfully")
        else:
            st.warning("Alert already set for the selected configurations")


        # else:
        #     if(temp and weather_type):
        #         record["temp"]=temp_conversion_to_Kelvin[temp_type](float(temp))
        #         record["weather_type"]=weather_type
        #     elif(weather_type):
        #         record["weather_type"]=weather_type
        #         record["temp"]=None
        #     elif(temp):
        #         record["temp"]=temp_conversion_to_Kelvin[temp_type](float(temp))
        #         record["weather_type"]=None
        #     # write code to update the record in the database
        #     mongo.db.alerts.update_one({"city": city}, {"$set": record})
        #     st.success("Alert updated successfully")

def delete_alert():
    st.title("Delete Alerts")
    with st.form("delete_alert"):
        city = st.selectbox("Select city", cities)
        temp_type = st.selectbox('Select temperature units in which the alert was set', ['Kelvin', 'Celsius', 'Fahrenheit'])
        temp = st.text_input("Enter the temperature (numerics) above which the alert was set")
        weather_type = st.selectbox("Select weather type for alert", different_weather_types, index=None, placeholder="Select")
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        query = {"city": city}
        if temp:
            try:
                converted_temp = temp_conversion_to_Kelvin[temp_type](float(temp))
                query["temp"] = converted_temp
            except ValueError:
                st.error("Please enter a valid numeric temperature.")
                return
        if weather_type:
            query["weather_type"] = weather_type
        else:
            query["weather_type"] = None

        # st.write("Query:", query)
        record = mongo.db.alerts.find_one(query)
        # st.write(record)

        if record:
            mongo.db.alerts.delete_one({"_id": record["_id"]})
            st.success("Alert deleted successfully")
        else:
            st.error("Alert not found")

def display_all_alerts():
    st.title("All Alerts")
    with st.form("display_all_alerts"):
        select_temp_units=st.selectbox("Select the temperature units in which the alert should be displayed", ['Kelvin', 'Celsius', 'Fahrenheit'])
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        alerts=mongo.db.alerts.find()
        d={"City":[], "Temperature":[], "Weather Type":[]}
        for alert in alerts:
            d['City'].append(alert['city'])
            if(alert['temp']):
                d['Temperature'].append(temp_conversion[select_temp_units](alert['temp']))
            else:
                d['Temperature'].append(None)
            
            if(alert['weather_type']):
                d['Weather Type'].append(alert['weather_type'])
            else:
                d['Weather Type'].append(None)
        new = pd.DataFrame.from_dict(d)
        st.table(new)


def delete_all_data():
    st.title("Delete All Rules")
    with st.form("delete_all_rules"):
        st.write("Click the submit button to delete all rules")
        submitted_form = st.form_submit_button("Submit")
        if submitted_form:
            mongo.db.updates.delete_many({})
            st.success("All records deleted successfully")        


def display_daily_summary():
    st.title("Display Daily Summary")
    with st.form("display_daily_summary"):
        city=st.selectbox("Select city", cities)
        temp_type=st.selectbox('Select temperature type', ['Kelvin', 'Celsius', 'Fahrenheit'])
        time_frame = st.selectbox('Select time frame', ['Last 7 Days', 'Last 30 Days', 'Full Data'])
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if city=="Delhi":
                daily_summaries = mongo.db.daily_summaries_delhi.find()
            elif city=="Mumbai":
                daily_summaries = mongo.db.daily_summaries_mumbai.find()
            elif city=="Chennai":
                daily_summaries = mongo.db.daily_summaries_chennai.find()
            elif city=="Bangalore":
                daily_summaries = mongo.db.daily_summaries_bangalore.find()
            elif city=="Kolkata":
                daily_summaries = mongo.db.daily_summaries_kolkata.find()
            elif city=="Hyderabad":
                daily_summaries = mongo.db.daily_summaries_hyderabad.find()
            d={"Date":[], "Average Temperature":[], "Maximum Temperature":[], "Minimum Temperature":[], "Dominant Condition":[], "Average Humidity":[], "Average Wind Speed":[]}
            for daily_summary in daily_summaries:
                d['Date'].append(daily_summary['date'])
                d['Average Temperature'].append(temp_conversion[temp_type](daily_summary['avg_temp']))
                d['Maximum Temperature'].append(temp_conversion[temp_type](daily_summary['max_temp']))
                d['Minimum Temperature'].append(temp_conversion[temp_type](daily_summary['min_temp']))
                d['Dominant Condition'].append(daily_summary['dominant_condition'])
                d['Average Humidity'].append(daily_summary['avg_humidity'])
                d['Average Wind Speed'].append(daily_summary['avg_wind_speed'])
            new = pd.DataFrame.from_dict(d)
            if(time_frame=="Last 7 Days"):
                new=new.tail(7)
            elif(time_frame=="Last 30 Days"):
                new=new.tail(30)
            st.table(new)

            st.subheader("Graphical Representation of the data")
            # Plotting the graphs in a 3x2 grid
            fig, axs = plt.subplots(3, 2, figsize=(18, 12))
            fig.suptitle(f'{city} Weather Summary ({time_frame})', fontsize=16)

            # Date vs Average Temperature
            axs[0, 0].plot(new['Date'], new['Average Temperature'], marker='o')
            axs[0, 0].set_title('Date vs Average Temperature')
            axs[0, 0].set_xlabel('Date')
            axs[0, 0].set_ylabel(f'Average Temperature ({temp_symbol[temp_type]})')
            axs[0, 0].grid(True)

            # Date vs Maximum Temperature
            axs[0, 1].plot(new['Date'], new['Maximum Temperature'], marker='o', color='red')
            axs[0, 1].set_title('Date vs Maximum Temperature')
            axs[0, 1].set_xlabel('Date')
            axs[0, 1].set_ylabel(f'Maximum Temperature ({temp_symbol[temp_type]})')
            axs[0, 1].grid(True)

            # Date vs Minimum Temperature
            axs[1, 0].plot(new['Date'], new['Minimum Temperature'], marker='o', color='blue')
            axs[1, 0].set_title('Date vs Minimum Temperature')
            axs[1, 0].set_xlabel('Date')
            axs[1, 0].set_ylabel(f'Minimum Temperature ({temp_symbol[temp_type]})')
            axs[1, 0].grid(True)

            # Bar graph for Dominant Condition
            dominant_conditions = new['Dominant Condition'].value_counts()
            axs[1, 1].bar(dominant_conditions.index, dominant_conditions.values, color='green')
            axs[1, 1].set_title('Dominant Weather Conditions')
            axs[1, 1].set_xlabel('Condition')
            axs[1, 1].set_ylabel('Frequency')

            axs[2, 0].plot(new['Date'], new['Average Humidity'], marker='o', color='orange')
            axs[2, 0].set_title('Date vs Average Humidity')
            axs[2, 0].set_xlabel('Date')
            axs[2, 0].set_ylabel('Average Humidity (%)')
            axs[2, 0].grid(True)

            axs[2, 1].plot(new['Date'], new['Average Wind Speed'], marker='o', color='purple')
            axs[2, 1].set_title('Date vs Average Wind Speed')
            axs[2, 1].set_xlabel('Date')
            axs[2, 1].set_ylabel('Average Wind Speed (m/s)')
            axs[2, 1].grid(True)

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            st.pyplot(fig)


            # st.line_chart(new.set_index("Date")["Average Temperature"])


def display_alerts():
    st.title("Past Triggered Alerts")
    with st.form("display_alerts"):
        time_frame = st.selectbox('Select the number of alerts to display', ['Last 7 Alerts', 'Last 30 Alerts', 'All Alerts'])
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        alerts=mongo.db.alerts_store.find()
        d={"Triggered on: Date":[], "Triggered at: Time":[], "Alert":[]}
        for alert in alerts:
            d['Triggered on: Date'].append(alert['date'])
            d['Triggered at: Time'].append(alert['time'])
            d['Alert'].append(alert['Alert'])
        new = pd.DataFrame.from_dict(d)
        if(time_frame=="Last 7 Alerts"):
            new=new.tail(7)
        elif(time_frame=="Last 30 Alerts"):
            new=new.tail(30)
        st.table(new)


def start_background_processes():
    if 'processes_started' not in st.session_state:
        st.session_state['processes_started'] = False

    if not st.session_state['processes_started']:
        # starting these two processes in the background, they run continuously
        process_1 = Process(target=background_data_fetch) # Function to fetch data using the API and storing it in the database as necessary
        process_2 = Process(target=check_alerts) # Function to check for if the alert conditions are met and if so then alert the user

        process_1.start()
        process_2.start()

        st.session_state['processes_started'] = True
        print("Background processes started")

if __name__ == "__main__":
    # Start the background processes when the script first runs
    start_background_processes()

    with st.sidebar:
        st.write("# Select")

    menu = ["Know the Weather", "Display Daily Summary", "Alerts"]
    choice = st.sidebar.selectbox("", menu)

    if choice == "Know the Weather":
        home()  # Function to display weather information
    elif choice == "Display Daily Summary":
        display_daily_summary()  # Function to display daily summary
    elif choice == "Alerts":
        alerts()  # Function to display alerts
        display_all_alerts() # Function to display all the alerts
        delete_alert() # Function to delete a specific alert
        display_alerts()  # Function to display all previously triggered alerts