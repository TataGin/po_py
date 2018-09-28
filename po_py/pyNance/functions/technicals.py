import pandas as pd
import numpy as np


def sma(levels, window):
    
    """ Simple Moving Average
        
        Posittional arguments:
        :levels - DataFrame
        :window - Int
     
        Returns:
        :DataFrame 
    
    """
    
    return levels.rolling(window, min_periods=window, center=False, win_type=None, on=None, axis=0, closed=None).mean().dropna()

    
def ema(levels, window):
    
    """ Exponential Moving Average 
    
        First value = Simple moving average
        Next values = [Close - EMA(previous day)] x Multiplier + EMA(previous day)
        Multiplier = 2 / (window + 1) 
        
        Posittional arguments:
        :levels - DataFrame
        :window - Int
        
        Returns:
        :DataFrame
    
    """
    
    levels = levels.copy()
    levels.iloc[window-1] = np.mean(levels[:window])
    levels = levels[window-1:]
    
    return levels.ewm(span=window, adjust=False, ignore_na=False, axis=0).mean()


def bollinger(levels, ma='sma', window=20, nb_std=2):
    
    """ Bollinger Indicator
    
        Positional arguments:
        :levels - DataFrame
        
        Keyword arguments:
        : ma - Defaults 'sma' - string
        :window - Defaults 20 - int
        : nb_std - Defaults 20 - int or float
    
        Returns:
        :dict of DataFrames {"Lower", "MA", "Upper"}
        
    """
    
    # Calculate Moving Averageg depending on user input
    ma = ma.lower().strip()
    if ma == 'sma':
        ma = sma(levels, window)
    elif ma == 'ema':
        ma = ema(levels, window)
        
    std = levels.rolling(window, min_periods=window).std()[window-1:]
    lower_band = ma - nb_std * std
    upper_band = ma + nb_std * std
    
    return {"lower" : lower_band, "ma" : ma, "upper" : upper_band}


def bol_band(bollinger):
    
    """ Bollinger Bandwidth
    
        = (Upper Band - Lower Band) / Moving Average 
        
        Positional arguments:
        :bollinger - DataFrame
        
        Returns:
        :DataFrame
    
    """
    
    return (bollinger["Upper"] - bollinger["Lower"]) / bollinger["MA"] * 100


def pct_b(levels, bollinger):
    
    """ %B Indicator
        
        = (Price - Lower Band) / (Upper Band - Lower Band)
        
        Positional arguments:
        : levels - DataFrame
        : bollinger - DataFrame
        
        Returns:
        :DataFrame 
    
    """
    
    return ((levels - bollinger["Lower"]) / (bollinger["Upper"] - bollinger["Lower"])).dropna()


def rsi(levels, window=14):
    
    """ Relative Strength Indicator (RSI)
    
        = 100 - (100 / 1 + RS) 
            
        RS = Average Gain / Average Loss
            
        First Avergae Gain = Sum(Max(0, Gain)) / window
        Next Average Gains = [Gain + Previous Average Gain x (window - 1)] / window 
            
        Same for Average Loss with Min instead of Max
            
        If avg gain = 0 then RSI = 0
        IF avg loss = 0 then RSI = 100 
        
        Positional arguments:
        :levels - DataFrame
        :window - int
        
        Returns:
        :DataFrame 
        
    """
    
    delta = levels.diff().dropna()
    
    avg_gain = delta[delta > 0].fillna(value=0)
    avg_gain.iloc[window - 1] = np.mean(avg_gain[:window])
    avg_gain = avg_gain[window - 1:]
    
    avg_loss = - delta[delta < 0].fillna(value=0)
    avg_loss.iloc[window - 1] = np.mean(avg_loss[:window])
    avg_loss = avg_loss[window - 1:]
    
    rs = avg_gain.ewm(com=window-1, adjust=False).mean() / avg_loss.ewm(com=window-1, adjust=False).mean()
    
    return 100 - 100 / (1 + rs)


def macd(levels, shortwind=12, longwind=26, signwind=9):

    """ Moving Average Convergence Divergence (MACD)
    
        MACD Line = Short EMA - Long EMA 
        Signal = x-Day EMA of MACD Line
        Histogram = MACD Line - Signal
        
        Positional arguments:
        :levels - DataFrame
        
        Keyword arguments:
        :shortwind - Defaults 12 - int
        :longwind - Defaults 26 - int
        :signwind - Defaults 9 - int
        
        Returns:
        :dict of DataFrames - {"MACD", "Signal", "Histogram"}
        
    """
    
    macd_line = ema(levels, shortwind)[longwind-shortwind:] - ema(levels, longwind)
    signal = ema(macd_line, signwind)
    histo = macd_line - signal
    
    return {"MACD" : macd_line[signwind-1:], "Signal" : signal, "Histogram" : histo[signwind-1:]}


def aroon(high, low, window=25):
    
    """ aroon(highs, lows, window=25)
    
        Aroon Up = 100 x (window - Days Since window-day High) / window
        Aroon Down = 100 x (window - Days Since window-day Low) / window
        Aroon Oscillator = Aroon-Up  -  Aroon-Down
        
        Positional arguments:
        :highs
        :lows
        
        Keyword arguments:
        :window - Defaults 25 - int
        
        Returns:
        :dict of DataFrames - {'Up', "Down", 'Oscillator'}
    
    """
        
    up = (100 * high.rolling(window).apply(lambda x: x.argmax() + 1) / window) [window-1:]
    down = (100 * low.rolling(window).apply(lambda x: x.argmin() + 1) / window) [window-1:]
    osc = up - down
        
    return {'Up' : up, "Down" : down, 'Oscillator' : osc}


def stoch(close, high, low, window=14, smawind=3, smoothwind=1):
    
    """ stoch(close, high, low, window=14, smawind=3, smoothwind=1)
    
        %K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
        %D = 3-day SMA of %K

        Lowest Low = lowest low for the look-back period
        Highest High = highest high for the look-back period 
        
        Positional arguments:
        :close - DataFrame
        :high - DataFrame
        :low - DataFrame
        
        Keyword arguments:
        :window - defaults 14 - int
        :smawind - defaults 3 - int
        :smoothwind - defaults 1 - int
        
        Returns:
        :dict of DataFrames - {'pct_k' : 'pct_d'}
    
    """
    
    pct_k = sma((close - low.rolling(window).min()) / (high.rolling(window).max() - low.rolling(window).min()) * 100, smoothwind)
    pct_d = sma(pct_k, smawind)
    
    return {'pct_k' : pct_k, 'pct_d' : pct_d}

