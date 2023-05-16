#imports required libraries AC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
warnings.filterwarnings("ignore")


# Fetch data from a server using the specified URL and parameters AC
url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical"
# may 8 2022 - may 8 2023 (unix time conversions) AC
param = {"convert":"USD","id":"7653","time_end":"1683504000","time_start":"1651968000"}
content = requests.get(url=url, params=param).json()
# Normalise the JSON response and store it in a DataFrame AC
df = pd.json_normalize(content['data']['quotes'])
# Prints the first few rows of the DataFrame AC
print(df.head)
# Prints the column names of the DataFrame before making any changes AC
print("values before changes:\n",(list(df.columns.values)))
# Extracting and renaming the important variables AC
df['Date']=pd.to_datetime(df['quote.USD.timestamp']).dt.tz_localize(None)
df['Low'] = df['quote.USD.low']
df['High'] = df['quote.USD.high']
df['Open'] = df['quote.USD.open']
df['Close'] = df['quote.USD.close']
df['Volume'] = df['quote.USD.volume']

# Drop original and redundant columns AC
df=df.drop(columns=['time_open','time_close','time_high','time_low', 'quote.USD.low', 'quote.USD.high', 'quote.USD.open', 'quote.USD.close', 'quote.USD.volume', 'quote.USD.market_cap', 'quote.USD.timestamp'])

# Creating a new feature for better representing day-wise values AC
df['Mean'] = (df['Low'] + df['High'])/2
# Converts Mean from USD -> EUR AC
df['Mean']=df["Mean"]/1.09
# Cleaning the data for any NaN or Null fields AC
df = df.dropna()



# Creating a copy for making small changes AC
dataset_for_prediction = df.copy()
# Shifts mean values by one day and stores in 'Actual' AC
dataset_for_prediction['Actual']=dataset_for_prediction['Mean'].shift()
# Cleaning the data for any NaN or Null fields AC
dataset_for_prediction=dataset_for_prediction.dropna()

# date time typecast
dataset_for_prediction['Date'] =pd.to_datetime(dataset_for_prediction['Date'])
dataset_for_prediction.index= dataset_for_prediction['Date']

from statsmodels.tsa.vector_ar.var_model import VAR

#predictiion
data=df[['Mean','Close']]
data=np.array(data,dtype='float32')
data=data[:2500]

# Exogenous variables
# Prepares the exogenous variables for VAR modeling by selecting columns and converting them to numpy arrays AC
exo=df[['Open']]
exo=np.array(exo,dtype='float32')
exo=exo[:2500,:]
# Creates a VAR model instance with the prepared data and exogenous variables AC
model=VAR(data,exog=exo)
# Sets the index of the model to the 'Date' column from the original DataFrame AC
x=np.array(df['Date'])
model.index=x[:2500]
# Fits the VAR model to the data AC
result=model.fit()
# Extracts the mean values from the original DataFrame and store them in the 'arr' variable AC
arr=np.array(df['Mean'])

#test data
# Sets the parameters for the test data AC
N=365
ap=arr[-N:]
z=exo[-N:,:]
# Forecasts using the VAR model to obtain predictions for the test data AC
a2=result.forecast(model.endog,N,z);
act=a2[:,1:]

# Prints the column names of the DataFrame after making changes AC
print("values after changes:\n",(list(df.columns.values)))
#VAR model call
print("VAR")
# Plot the predicted and actual values using matplotlib AC
plt.plot(act,color='#32a7f8',label='predicted')
plt.plot(ap,color='hotpink',label='actual')
# Calculate the RMSE between the predicted and actual values AC
c=0
for i in range(N):
   c+=(act[i]-ap[i])**2
c/=N


#print RMSE AC
print("RMSE",c**0.5)
# Plot the predicted and actual values using matplotlib AC
plt.xlabel('Days')
plt.ylabel('Value')
plt.legend()
plt.show()

