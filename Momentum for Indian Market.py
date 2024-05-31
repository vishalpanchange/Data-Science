#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install yfinance')


# In[7]:


import plotly.express as px
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


# In[8]:


# Step 1: Data Collection
# Define the list of Indian stocks (tickers)
tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS']  # Add more tickers as needed

# Define the time period for historical data
start_date = datetime.now() - timedelta(days=365*5)  # Last 5 years
end_date = datetime.now()

# Download the historical data
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']


# In[9]:


# Step 2: Data Preparation
# Handle missing values by forward filling
data.fillna(method='ffill', inplace=True)


# In[10]:


# Step 3: Momentum Calculation
# Calculate returns over the look-back period (e.g., 12 months)
look_back_period = 252  # Approx 1 year of trading days
momentum = data.pct_change(look_back_period)


# In[11]:


# Step 4: Ranking and Selection
# Rank the stocks based on momentum
momentum_rank = momentum.rank(axis=1, ascending=False)

# Select top N stocks (e.g., top 10)
N = 10
top_momentum_stocks = momentum_rank.apply(lambda x: x <= N, axis=1)


# In[12]:


# Step 5: Index Construction
# Create the portfolio by assigning equal weights to selected stocks
weights = top_momentum_stocks.div(top_momentum_stocks.sum(axis=1), axis=0).fillna(0)

# Calculate the daily portfolio returns
portfolio_returns = (data.pct_change() * weights.shift(1)).sum(axis=1)


# In[13]:


# Step 6: Backtesting
# Calculate cumulative returns
cumulative_returns = (1 + portfolio_returns).cumprod()

# Plot the cumulative returns using Plotly
fig = px.line(cumulative_returns, title='Momentum Portfolio Cumulative Returns', labels={'value': 'Cumulative Returns', 'index': 'Date'})
fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Returns')
fig.show()


# ## This increase suggests that the momentum strategy has performed exceptionally well during this period. Several factors could contribute to this trend, including market recovery post-COVID-19, economic stimulus measures, and increased investor confidence.
# 

# In[ ]:




