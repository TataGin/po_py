
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:



        


# In[2]:


def sma(levels, window):
    
    """ sma(levels, window)
        = rolling simple average
        
        Returns DataFrame"""
    
    return levels.rolling(window, min_periods=window, center=False, win_type=None, on=None, axis=0, closed=None).mean().dropna()


# In[3]:


def ema(levels, window):
    
    """ ema(levels, window) 
    
    First value = Simple moving average
    Next values = [Close - EMA(previous day)] x Multiplier + EMA(previous day)
    Multiplier = 2 / (window + 1) 
    
    Returns DataFrame"""
    
    levels = levels.copy()
    levels.iloc[window-1] = np.mean(levels[:window])
    levels = levels[window-1:]
    
    return levels.ewm(span=window, adjust=False, ignore_na=False, axis=0).mean()


# In[4]:


def bollinger(levels, ma='SMA', window=20, nb_std=2):
    
    """ bollinger(levels, ma='SMA', window=20, nb_std=2)
    
    = ma +/- nb_std * std
    
    Returns {"Lower", "MA", "Upper"} """
    
    # Calculate Moving Averageg depending on user input
    ma = ma.lower().strip()
    if ma == 'sma':
        ma = sma(levels, window)
    elif ma == 'ema':
        ma = ema(levels, window)
        
    std = levels.rolling(window, min_periods=window).std()[window-1:]
    lower_band = ma - nb_std * std
    upper_band = ma + nb_std * std
    
    return {"Lower" : lower_band, "MA" : ma, "Upper" : upper_band}


# In[5]:


def bol_band(bollinger):
    
    """ bol_band(bollinger)
    
    = (Upper Band - Lower Band) / Moving Average 
    
    Returns DataFrame"""
    
    return (bollinger["Upper"] - bollinger["Lower"]) / bollinger["MA"] * 100


# In[6]:


def pct_b(levels, bollinger):
    
    """ pct_B(levels, bollinger)
        
    = (Price - Lower Band) / (Upper Band - Lower Band)
    
    Returns DataFrame """
    
    return ((levels - bollinger["Lower"]) / (bollinger["Upper"] - bollinger["Lower"])).dropna()


# In[14]:


def rsi(levels, window=14):
    
    """ rsi(levels, window=14)
    
    = 100 - (100 / 1 + RS) 
        
    RS = Average Gain / Average Loss
        
    First Avergae Gain = Sum(Max(0, Gain)) / window
    Next Average Gains = [Gain + Previous Average Gain x (window - 1)] / window 
        
    Same for Average Loss with Min instead of Max
        
    If avg gain = 0 then RSI = 0
    IF avg loss = 0 then RSI = 100 
    
    Returns DataFrame """
    
    delta = levels.diff().dropna()
    
    avg_gain = delta[delta > 0].fillna(value=0)
    avg_gain.iloc[window - 1] = np.mean(avg_gain[:window])
    avg_gain = avg_gain[window - 1:]
    
    avg_loss = - delta[delta < 0].fillna(value=0)
    avg_loss.iloc[window - 1] = np.mean(avg_loss[:window])
    avg_loss = avg_loss[window - 1:]
    
    rs = avg_gain.ewm(com=window-1, adjust=False).mean() / avg_loss.ewm(com=window-1, adjust=False).mean()
    
    return 100 - 100 / (1 + rs)


# In[15]:


def macd(levels, shortwind=12, longwind=26, signwind=9):

    """ macd(levels, shortwind=12, longwind=26, signwind=9) 
    
    MACD Line = Short EMA - Long EMA 
    Signal = x-Day EMA of MACD Line
    Histogram = MACD Line - Signal 
    
    Returns {"MACD", "Signal", "Histogram"} """
    
    macd_line = ema(levels, shortwind)[longwind-shortwind:] - ema(levels, longwind)
    signal = ema(macd_line, signwind)
    histo = macd_line - signal
    
    return {"MACD" : macd_line[signwind-1:], "Signal" : signal, "Histogram" : histo[signwind-1:]}


# In[16]:


def aroon(high, low, window=25):
    
    """ aroon(highs, lows, window=25)
    
    Aroon Up = 100 x (window - Days Since window-day High) / window
    Aroon Down = 100 x (window - Days Since window-day Low) / window
    Aroon Oscillator = Aroon-Up  -  Aroon-Down 
    Returns {'Up', "Down", 'Oscillator'} """
        
    up = (100 * high.rolling(window).apply(lambda x: x.argmax() + 1) / window) [window-1:]
    down = (100 * low.rolling(window).apply(lambda x: x.argmin() + 1) / window) [window-1:]
    osc = up - down
        
    return {'Up' : up, "Down" : down, 'Oscillator' : osc}


# In[17]:


def stoch(close, high, low, window=14, smawind=3, smoothwind=1):
    
    """ stoch(close, high, low, window=14, smawind=3, smoothwind=1)
    
    %K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
    %D = 3-day SMA of %K

    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period 
    
    Returns {'pct_k' : 'pct_d'} """
    
    pct_k = sma((close - low.rolling(window).min()) / (high.rolling(window).max() - low.rolling(window).min()) * 100, smoothwind)
    pct_d = sma(pct_k, smawind)
    
    return {'pct_k' : pct_k, 'pct_d' : pct_d}

