# -*- coding: utf-8 -*-
"""ARIMA MODELS IN Time Series Modelling- Masole.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RFnHyu3Xf4DsLQ_62eqBIb3MChW-HEez

**IMPORTING RELEVANT DEPENDENCIES**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""1. **Data Preprocessing:**

**UPLOADING DATA SET FILE AS COMMA SEPERATED VALUE FILE AND TRANSFORM IT INTO A DATA FRAME**
"""

file_path="/content/time_series_covid19_confirmed_US.csv"
Covid_con=pd.read_csv(file_path) #DATA FRAME CONTAINING COFIRMED COVID CASES IN USA

filepath="/content/time_series_covid19_deaths_US.csv"
Covid_death=pd.read_csv(file_path) #DATA FRAME CONTAINING COVID DEATH TOLL IN USA

print(Covid_con.info())

print(Covid_con.columns)

print(Covid_con.head())

# Assuming your DataFrame is named Covid_con
# Replace 'US' with the actual state or region you are interested in
state_data = Covid_con[Covid_con['Province_State'] == 'US']

# Columns to drop
columns_to_drop = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2']

# Drop specified columns
state_data = state_data.drop(columns=columns_to_drop)

# Display the resulting DataFrame
print(state_data)

print(Covid_con.head(5))

"""2. **DESCRIPTIVE ANALYSIS**

**The purpose of this code is to list and display all the unique values present in the 'Province_State' column of the Covid_con DataFrame. It provides a quick overview of the different province states represented in the dataset**
"""

us_states = Covid_con['Province_State'].unique()

print("List of all Province_States in the United States:")
for state in us_states:
    print(state)

"""**The code cell below provide insights into the COVID-19 data by state. It calculates the total confirmed cases for each state, identifies the state with the highest and lowest cases, and prints the total confirmed cases for each state in descending order. This type of analysis helps in understanding the distribution of COVID-19 cases across different states and identifying states with significant case numbers**"""

# Extract date columns and corresponding confirmed cases for each state
date_columns = Covid_con.columns[11:]
state_cases = Covid_con.groupby('Province_State')[date_columns].sum()

# Calculate total cases for each state
total_cases_per_state = state_cases.iloc[:, -1]  # Assuming the last date column represents the latest date

# Identify state with the highest and lowest cases
state_highest_cases = total_cases_per_state.idxmax()
state_lowest_cases = total_cases_per_state.idxmin()

# Print the counts
print("Total confirmed cases by state:")
print(state_cases.sum(axis=1).sort_values(ascending=False))

# Print the results
print("\nState with the highest recorded cases: ", state_highest_cases)
print("Total cases: ", total_cases_per_state[state_highest_cases])

print("\nState with the lowest recorded cases: ", state_lowest_cases)
print("Total cases: ", total_cases_per_state[state_lowest_cases])

"""3.**VISUAL ANALYSIS**"""

# Extract date columns and corresponding confirmed cases for California
california_cases = Covid_con[Covid_con['Province_State'] == 'California'][date_columns].sum()

# Convert the index (date) to datetime format
california_cases.index = pd.to_datetime(california_cases.index)

# Resample the data on a weekly basis and sum the confirmed cases
weekly_california_cases = california_cases.resample('W').sum()

# Plot the weekly trends
plt.figure(figsize=(12, 6))
plt.plot(weekly_california_cases, marker='o', linestyle='-', color='b')
plt.title('Weekly Trends in Confirmed Cases for California')
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.grid(True)
plt.show()

"""**CALIFORNIA IS THE PROVINCE STATE WITH THE MOST RECORDED NUMBER OF CONFIRMED COVID 19 CASES AND THE DEATH TOLL. THE PLOT ABOVE SHOW THAT BEGINNING MAY 2020 THERE HAS BEEN AN INCREASING TREND IN CONFIRMED CASES, MORE ESPECIALLY DURING THE COLD SEASON MONTHS WHERE STEEP INCREASES IN COVID CONFIRMED CASES ARE CAPTURED BY THE PLOT. THE STEEP INCREASES IN COVID 19 CASES DURING THE COLD MONTHS IS A RESULT OF THE TRANSMISSION NATURE OF THE VIRUS.DURING COLD SEASONS WHEN PEOPLE`s IMMNUNE SYSTEMS ARE PRONE TO ILLNESS AND BODIES BECOME MORE SUSCEPTIBLE TO INFECTIONS LIKE COVID19 AND THAT IS HOW THEY CONSULT AT HEALTH CARE FACILITIES.**"""

# Resample the data on a monthly basis and sum the confirmed cases
monthly_california_cases = california_cases.resample('M').sum()

# Plot the monthly trends
plt.figure(figsize=(12, 6))
plt.plot(monthly_california_cases, marker='o', linestyle='-', color='b')
plt.title('Monthly Trends in Confirmed Cases for California')
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.grid(True)
plt.show()

# Extract date columns and corresponding confirmed cases for California
california_cases = Covid_con[Covid_con['Province_State'] == 'California'][date_columns].sum()

# Print the first few rows
print(california_cases.head())

# Print summary statistics
print(california_cases.describe())

"""
25% (Q1): This indicates that 25% of the recorded days have confirmed cases below 951,832.

50% (Q2 or Median): The median is the middle value when the data is sorted. In this case, 50% of the recorded days have confirmed cases below 4.23 million.

75% (Q3): This tells us that 75% of the recorded days have confirmed cases below 9.56 million.

Maximum Value: The maximum value in the dataset is approximately 12.13 million, suggesting that on the day with the highest recorded cases, the number reached this value."""

# Extract date columns and corresponding confirmed cases for California
california_cases = Covid_con[Covid_con['Province_State'] == 'California'][date_columns].sum()

# Create a boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(california_cases, vert=False, widths=0.7, patch_artist=True)
plt.title('Boxplot of Confirmed Cases for California')
plt.xlabel('Confirmed Cases')
plt.yticks([1], ['California'])
plt.show()

pip install geopy

"""**The purpose of this code is to identify and print the top 5 states closest to California based on geographical coordinates. It utilizes the Haversine formula through the geodesic function to calculate the distances between California and other states. This type of analysis can be useful for understanding the proximity of states and may have relevance in various contexts, such as regional comparisons or logistics planning.**"""

from geopy.distance import geodesic

# Assuming your DataFrame is named Covid_con
# Extract coordinates for California
california_coords = Covid_con.loc[Covid_con['Province_State'] == 'California', ['Lat', 'Long_']].iloc[0]

# Calculate distances to other states
state_distances = {}
for state in Covid_con['Province_State'].unique():
    if state != 'California':
        state_coords = Covid_con.loc[Covid_con['Province_State'] == state, ['Lat', 'Long_']].iloc[0]
        distance = geodesic((california_coords['Lat'], california_coords['Long_']), (state_coords['Lat'], state_coords['Long_'])).kilometers
        state_distances[state] = distance

# Sort states by distance
sorted_states = sorted(state_distances.items(), key=lambda x: x[1])

# Print the closest states
print("Top 5 states closest to California:")
for state, distance in sorted_states[:5]:
    print(f"{state}: {distance:.2f} kilometers")

"""**The purpose of this code is to visualize and compare the weekly trends in confirmed COVID-19 cases for a selected set of states. The plot allows for easy comparison of how the confirmed cases have evolved over time on a weekly basis for each state. Resampling the data on a weekly basis can help in identifying trends and patterns, especially when dealing with time-series data**"""

# Define the states of interest
target_states = ['Nevada', 'Idaho', 'Oregon', 'Utah', 'Washington']

# Extract and plot confirmed cases for the selected states
plt.figure(figsize=(12, 6))

for state in target_states:
    state_cases = Covid_con[Covid_con['Province_State'] == state][date_columns].sum()
    state_cases.index = pd.to_datetime(state_cases.index)

    # Resample the data on a weekly basis and sum the confirmed cases
    weekly_state_cases = state_cases.resample('W').sum()

    # Plot the weekly trends
    plt.plot(weekly_state_cases, label=state)

plt.title('Weekly Trends in Confirmed Cases for Selected States')
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend()
plt.grid(True)
plt.show()

"""**CODE BELOW WILL PRODUCE OUTPUT IN FORM A CORRELATION MAP BETWEEN PROXIMITY TO STATE WITH MOST CASES RECORDED AND TREND IN CONFIRMED CASES**"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Extract coordinates for California
california_coords = Covid_con.loc[Covid_con['Province_State'] == 'California', ['Lat', 'Long_']].iloc[0]

# Calculate distances and sort states by distance
state_distances = {}
for state in Covid_con['Province_State'].unique():
    if state != 'California':
        state_coords = Covid_con.loc[Covid_con['Province_State'] == state, ['Lat', 'Long_']].iloc[0]
        distance = geodesic((california_coords['Lat'], california_coords['Long_']), (state_coords['Lat'], state_coords['Long_'])).kilometers
        state_distances[state] = distance

# Sort states by distance
sorted_states = sorted(state_distances.items(), key=lambda x: x[1])

# Extract confirmed cases and distances for each state
confirmed_cases = []
distances = []

for state, distance in sorted_states:
    state_cases = Covid_con[Covid_con['Province_State'] == state][date_columns].sum().iloc[-1]
    confirmed_cases.append(state_cases)
    distances.append(distance)

# Calculate correlation coefficient
correlation_coefficient, _ = pearsonr(confirmed_cases, distances)

# Scatter plot with regression line
plt.figure(figsize=(10, 6))
plt.scatter(distances, confirmed_cases, color='blue', label='States')
plt.title('Correlation Between Distance from California and Confirmed Cases')
plt.xlabel('Distance from California (km)')
plt.ylabel('Confirmed Cases')
plt.grid(True)



plt.legend()
plt.show()

print(f'Correlation Coefficient: {correlation_coefficient:.2f}')

"""A correlation coefficient of -0.19 indicates a weak negative correlation between the distance from California and the number of confirmed COVID-19 cases"""

date_columns = Covid_con.columns[11:].to_list()

# Convert date columns to datetime format
date_columns_datetime = pd.to_datetime(date_columns)

# Find the first and last date
first_date = date_columns_datetime.min()
last_date = date_columns_datetime.max()

# Calculate the number of days captured in the data
days_captured = (last_date - first_date).days + 1

# Show beginning and ending months
beginning_month = first_date.strftime('%B %Y')
ending_month = last_date.strftime('%B %Y')

print(f"First Date: {first_date}")
print(f"Last Date: {last_date}")
print(f"Number of Days Captured: {days_captured} days")
print(f"Beginning Month: {beginning_month}")
print(f"Ending Month: {ending_month}")

"""**COVID DEATHS**"""

file_path="/content/time_series_covid19_deaths_US.csv"
Covid_death=pd.read_csv(file_path)

print(Covid_death.info())

print(Covid_death.columns)

"""2.**DESCRIPTIVE ANALYSIS**"""

# Grouping by 'Province_State' and summing up the deaths for each state
state_deaths = Covid_death.groupby('Province_State')['3/9/23'].sum().reset_index()

# Sorting the result in ascending order based on the total deaths
sorted_state_deaths = state_deaths.sort_values(by='3/9/23', ascending=True)

# Displaying the result
print(sorted_state_deaths)

"""3.**VISUAL ANALYSIS: AT NATIONAL LEVEL**

**The purpose of this code is to provide a visual representation of the total number of deaths for each state as of 3/9/23. The horizontal bar chart makes it easy to compare the death tolls across different states, with states sorted in ascending order based on the total number of deaths. This type of visualization is useful for understanding the distribution of COVID-19 fatalities among different states**
"""

# Grouping by 'Province_State' and summing up the deaths for each state
state_deaths = Covid_death.groupby('Province_State')['3/9/23'].sum().reset_index()

# Sorting the result in ascending order based on the total deaths
sorted_state_deaths = state_deaths.sort_values(by='3/9/23', ascending=True)

# Plotting the bar chart
plt.figure(figsize=(12, 8))
plt.barh(sorted_state_deaths['Province_State'], sorted_state_deaths['3/9/23'], color='skyblue')
plt.xlabel('Number of Deaths')
plt.ylabel('States')
plt.title('Total Deaths by State as of 3/9/23')
plt.show()

"""**The purpose of this code is to visually compare the total COVID-19 deaths between urban and rural areas. The bar chart provides a clear representation of the differences in death tolls based on the urban/rural classification**"""

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have the death toll data in a DataFrame named 'death_data'
data = {'Diamond Princess': 0.0, 'Grand Princess': 3.0, 'American Samoa': 34.0, 'Northern Mariana Islands': 41.0,
        'Guam': 420.0, 'District of Columbia': 1432.0, 'Alaska': 1486.0, 'Hawaii': 1841.0, 'North Dakota': 2470.0,
        'Maine': 2928.0, 'New Hampshire': 3003.0, 'South Dakota': 3190.0, 'Delaware': 3324.0, 'Montana': 3652.0,
        'Rhode Island': 3870.0, 'Nebraska': 4936.0, 'Idaho': 5416.0, 'Puerto Rico': 5823.0, 'New Mexico': 9061.0,
        'Oregon': 9373.0, 'Kansas': 10066.0, 'Iowa': 10725.0, 'Nevada': 11922.0, 'Connecticut': 12220.0,
        'Arkansas': 13020.0, 'Mississippi': 13370.0, 'Colorado': 14181.0, 'Minnesota': 14870.0, 'Maryland': 16544.0,
        'Oklahoma': 17972.0, 'Kentucky': 18130.0, 'Louisiana': 18766.0, 'South Carolina': 19600.0, 'Alabama': 21032.0,
        'Missouri': 22870.0, 'Massachusetts': 24333.0, 'Indiana': 26115.0, 'North Carolina': 28432.0,
        'Tennessee': 29263.0, 'Arizona': 33102.0, 'New Jersey': 36015.0, 'Illinois': 41496.0, 'Ohio': 41796.0,
        'Michigan': 42205.0, 'Georgia': 42489.0, 'Pennsylvania': 50398.0, 'New York': 77157.0, 'Florida': 86850.0,
        'Texas': 88906.0, 'California': 101159.0}

# Creating a DataFrame from the dictionary
death_data = pd.DataFrame(list(data.items()), columns=['State', 'Death Toll'])

#  (0 for rural, 1 for urban)
urban_rural_info = {'Diamond Princess': 0, 'Grand Princess': 0, 'American Samoa': 1, 'Northern Mariana Islands': 0,
                    'Guam': 1, 'District of Columbia': 1, 'Alaska': 0, 'Hawaii': 1, 'North Dakota': 0,
                    'Maine': 0, 'New Hampshire': 1, 'South Dakota': 0, 'Delaware': 1, 'Montana': 0,
                    'Rhode Island': 1, 'Nebraska': 0, 'Idaho': 0, 'Puerto Rico': 1, 'New Mexico': 0,
                    'Oregon': 1, 'Kansas': 0, 'Iowa': 0, 'Nevada': 1, 'Connecticut': 1, 'Arkansas': 0,
                    'Mississippi': 0, 'Colorado': 1, 'Minnesota': 0, 'Maryland': 1, 'Oklahoma': 0,
                    'Kentucky': 0, 'Louisiana': 1, 'South Carolina': 0, 'Alabama': 0, 'Missouri': 0,
                    'Massachusetts': 1, 'Indiana': 0, 'North Carolina': 1, 'Tennessee': 0, 'Arizona': 1,
                    'New Jersey': 1, 'Illinois': 1, 'Ohio': 1, 'Michigan': 1, 'Georgia': 1, 'Pennsylvania': 1,
                    'New York': 1, 'Florida': 1, 'Texas': 1, 'California': 1}

# Adding Urban_Rural column to death_data DataFrame
death_data['Urban_Rural'] = death_data['State'].map(urban_rural_info)

# Creating variables for urban and rural death tolls
urban_deaths = death_data[death_data['Urban_Rural'] == 1]['Death Toll']
rural_deaths = death_data[death_data['Urban_Rural'] == 0]['Death Toll']

# Plotting the bar chart
plt.bar(['Urban', 'Rural'], [urban_deaths.sum(), rural_deaths.sum()], color=['skyblue', 'lightgreen'])
plt.title('Total COVID-19 Deaths by Urban/Rural Classification')
plt.xlabel('Urban/Rural')
plt.ylabel('Total Deaths')
plt.show()

"""**TIME SERIES ANALYSIS: USING ARIMA MODELS TO GENERATE INSIGHT ABOUT DISEASE OUTBREAK IN THE USA**

**PERFOMING A STATIONARITY TEST: Technical analysis using Augmented Dickey Fuller test**

**Augmented Dickey-Fuller (ADF) test, which is commonly used in time series analysis to test for the presence of a unit root in a univariate time series. The ADF test is often used to check the stationarity of a time series.**

**The ADF statistic is a negative number that indicates how much the time series deviates from being a non-stationary process. The more negative the ADF statistic, the stronger the evidence against the presence of a unit root.**

**The p-value associated with the ADF statistic is used to determine the significance of the test. In hypothesis testing, a small p-value (typically below a chosen significance level, e.g., 0.05) suggests that there is enough evidence to reject the null hypothesis.**

**The results of the ADF test suggest that the COVID-19 outbreak data series is likely stationary**
"""

from statsmodels.tsa.stattools import adfuller
# Extract the time series data
time_series_data =Covid_death ['3/2/23']

# Step 3: Perform Augmented Dickey-Fuller test
result = adfuller(time_series_data)

# Step 4: Extract and print the results
adf_statistic = result[0]
p_value = result[1]

print(f'ADF Statistic: {adf_statistic}')
print(f'p-value: {p_value}')

"""**MODEL SELECTION: ANALYZING AUTO CORRELATION FUNCTION PLOTS**

"""

import statsmodels.api as sm
import matplotlib.pyplot as plt

fig, (subplot1, subplot2) = plt.subplots(2, 1, figsize=(8, 8))

sns.lineplot(x=Covid_death['3/2/23'],  y=Covid_death['3/6/23'], ax=subplot1)
sm.graphics.tsa.plot_acf(Covid_death['3/6/23'], lags=40, ax=subplot2)
fig.show()

from statsmodels.tsa.arima.model import ARIMA
ARMA_model = ARIMA(Covid_death['3/2/23'], order=(2, 0, 0)).fit()

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf

# Assuming you have a time series data in a pandas DataFrame named 'df'
# Replace 'your_column_name' with the actual column name containing the time series data

# Extract the time series data
time_series_data = Covid_death['3/2/23']

# Calculate autocorrelation values
acf_values = acf(time_series_data, nlags=40, fft=False)

# Plot the ACF
plt.stem(acf_values)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.show()

# Identify the point where ACF drops off
threshold = 3  # Adjust this threshold based on your data
q_value = next(i for i, acf_value in enumerate(acf_values) if abs(acf_value) < threshold)

print(f'Optimal q value: {q_value}')

# Assuming df is your DataFrame with the time series data
train_size = int(len(Covid_death) * 0.8)  # 80% for training, 20% for testing
train, test = Covid_death[:train_size], Covid_death[train_size:]

from statsmodels.tsa.arima.model import ARIMA

# Replace (p, d, q) with your chosen parameters
arima_order = (2, 0, 0)
arima_model = ARIMA(train['3/2/23'], order=arima_order).fit()

predictions = arima_model.predict(start=len(train), end=len(train) + len(test) - 1)

from sklearn.metrics import mean_squared_error
import numpy as np

mse = mean_squared_error(test['3/2/23'], predictions)
rmse = np.sqrt(mse)

print(f'Root Mean Squared Error (RMSE): {rmse}')

plt.plot(test['3/2/23'], label='Actual')
plt.plot(predictions, label='Predicted')
plt.legend()
plt.show()

"""**INSIGHT GENERATION**"""

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Example: assuming 'REGION' is a column indicating different regions
regions = Covid_death['Province_State'].unique()

# Function to forecast future cases and deaths for a given region
def forecast_for_region(region):
    region_data = Covid_death[Covid_death['Province_State'] == region].copy()

    # Assuming 'DATE' is the date column in your DataFrame
    # Replace 'your_column_name' with the actual column name containing the time series data
    time_series_data = region_data['Province_State']

    # Assuming your ARIMA model order is (p, d, q)
    # Replace (p, d, q) with the order you obtained from training the model
    arima_model = ARIMA(time_series_data, order=(2, 0, 0)).fit()

    # Forecast future values
    forecast_steps = 12  # Adjust based on your needs
    forecast = arima_model.get_forecast(steps=forecast_steps)

    # Extract forecasted values
    forecast_values = forecast.predicted_mean

    # Add forecasted values to the DataFrame
    region_data = region_data.append(pd.DataFrame(index=pd.date_range(start=region_data['2020-01-22'].max(), periods=forecast_steps + 1, freq='M')))
    region_data['Forecast'] = forecast_values.values

    return region_data