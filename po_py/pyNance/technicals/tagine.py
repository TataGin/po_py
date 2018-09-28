import sys
import pandas as pd
import numpy as np

sys.path.insert(0, 'C:/Users/F.Ginez/Code/Python/')

import PyNance.functions.technicals as tk


class TechIndicator:

    """ """
        
        
    sma_name = 'Simple Moving Average'
    ema_name = 'Exponential Moving Average'
    bollinger_name = 'Bollinger Band'
    bol_band_name = 'Bollinger Bands'
    pct_b_name = 'Bollinger Bandwidth'
    rsi_name = 'Relative Strength Indicator (RSI)'
    macd_name = 'Moving Average Convergence Divergence'
    aroon_name = 'Aroon Indicator'
    stoch_name = 'Stochastic Oscillator'
    

    def __init__(self, close=None, high=None, low=None,):
    
        self.close = close
        self.high = high
        self.low = low
    
        
    def get_name(self):
        return self.name
        
    
    def get_parameters(self):
        return self.parameters
        
        
    def get_values(self):
        return self.val
 
    
    def to_DB(self, userID, password, dsn):
    
        conn = sql.create_engine('mssql+pyodbc://'+userID+':'+password+'@'+dsn)
    
    
    def stack(self):
        
        stacked_data = {}
        for name, data in self.val.items():
            stacked_data[name] = data.stack().reset_index().set_index('Date')
            stacked_data[name].columns = ['Security', 'Value']
            stacked_data[name].insert(1, 'Indicator', self.name)
            stacked_data[name].insert(2, 'Sub Indicator', name)
        
        stacked_data = pd.concat([data for data in stacked_data.values()])
        
        stacked_param = pd.DataFrame.from_dict(self.parameters, 'index')
        stacked_param.index.name = 'Name'
        stacked_param.columns = ['Value']
        stacked_param.insert(1, 'Indicator', self.name)
        
        return stacked_data, stacked_param
    


class AllIndicators(TechIndicator):
    
    """ """
    
    def __init__(self, parameters, close=None, high=None, low=None):
        
        super().__init__(close=close)
        self.parameters = parameters
        
        
    def compute_all(self):
        ma = MovAvg(self.parameters['MA']['Window'],self.parameters['MA']['MA']).val
        ma = MA(self.parameters['MA']['Window'],self.parameters['MA']['MA']).val  
    
    
    
class MovAvg(TechIndicator):

    """ """
    
    
    def __init__(self, window, ma='sma', close=None):
    
        super().__init__(close=close)
        
        ma = ma.lower().strip()
        if ma == 'sma':
            self.name = self.sma_name
        elif ma == 'ema':
            self.name = self.ema_name
            
        self.parameters = {'Window':window, 'MA':ma}
        self._calc_ma(window, ma)
        self.val = {'Moving Average':self.ma}
        
    
    def _calc_ma(self, window, ma):
    
        """  """
        
        if ma == 'sma':
            tk.sma(self.close, window)
        elif ma == 'ema':
            tk.ema(self.close, window)


class Bollinger(TechIndicator):

    """ """

    def __init__(self, ma='sma', window=20, nb_std=2, close=None):
    
        super().__init__(close=close)
        
        ma = ma.lower().strip()
        self.name = self.bollinger_name
        self.parameters = {'MA':ma, 'Window':window, 'Nb Std':nb_std}
        self._calc_bollinger(ma, window, nb_std)
        self.val = {'MA':self.ma, 'Std':self.std, 'Lower Band':self.lower_band, 'Upper Band':self.upper_band, 'Bandwidth':self.bandwidth, 'Pct B':self.pct_b}
        
        
    def _calc_bollinger(self, ma, window, nb_std):
    
        temp = tk.bollinger(self.close, ma, window, nb_std)
        self.ma = temp('ma')
        self.lower_band = temp('lower')
        self.upper_band = temp('upper')
        
        self.bandwidth = tk.boll_band(temp)
        
        self.pct_b = pct_b(self.close, bollinger)
    
    
class RSI(TechIndicator):

    """ rsi(window=14)
    = 100 - (100 / 1 + RS) 
    
    RS = Average Gain / Average Loss
    
    First Avergae Gain = Sum(Max(0, Gain)) / window
    Next Average Gains = [Gain + Previous Average Gain x (window - 1)] / window 
    
    Same for Average Loss with Min instead of Max
    
    If avg gain = 0 then RSI = 0
    IF avg loss = 0 then RSI = 100 """
    
    
    def __init__(self, window=20, close=None):
    
        super().__init__(close=close)
        
        self.name = self.rsi_name
        self.parameters = {'Window':window} 
        self.calc_rsi(window)
        self.val = {'RSI': self.rsi}
        
    
    def calc_rsi(self, window):
    
        delta = self.close.diff().dropna()
    
        avg_gain = delta[delta > 0].fillna(value=0)
        avg_gain.iloc[window - 1] = np.mean(avg_gain[:window])
        avg_gain = avg_gain[window - 1:]
        
        avg_loss = - delta[delta < 0].fillna(value=0)
        avg_loss.iloc[window - 1] = np.mean(avg_loss[:window])
        avg_loss = avg_loss[window - 1:]
        
        rs = avg_gain.ewm(com=window-1, adjust=False).mean() / avg_loss.ewm(com=window-1, adjust=False).mean()
        
        self.rsi = 100 - 100 / (1 + rs)
    
    
    
class MACD(TechIndicator):

    """ macd( shortwind=12, longwind=26, signwind=9) 
    
    MACD Line = Short EMA - Long EMA 
    Signal = x-Day EMA of MACD Line
    Histogram = MACD Line - Signal 
    
    Returns {"MACD", "Signal", "Histogram"} """
    
    
    def __init__(self, shortwind=12, longwind=26, signwind=9, close=None):
    
        super().__init__(close=close)
        
        self.name = self.macd_name
        self.parameters = {'Short Window':shortwind, 'Long Window':longwind, 'Signal Window':signwind}
        self.calc_macd(shortwind, longwind, signwind, close)
        self.val = {'MACD':self.line, 'Signal':self.signal, "Histogram":self.histo}
        
    
    def calc_ma(self, window, close):
    
        return MovAvg(window, ma='ema', close=close).ma
        
    
    def calc_macd(self, shortwind, longwind, signwind, close):
    
        self.line = self.calc_ma(shortwind, self.close)[longwind-shortwind:] - self.calc_ma(longwind, self.close)
        self.signal = self.calc_ma(signwind, self.line)
        self.histo = self.line[signwind-1:] - self.signal
        


class Aroon(TechIndicator):

    """ aroon(window=25)
    
    Aroon Up = 100 x (window - Days Since window-day High) / window
    Aroon Down = 100 x (window - Days Since window-day Low) / window
    Aroon Oscillator = Aroon-Up  -  Aroon-Down 
    
    Returns {'Up', "Down", 'Oscillator'} """
    
    
    def __init__(self, window=25, high=None, low=None):
    
        super().__init__(high=high, low=low)
        
        self.name = self.aroon_name
        self.parameters = {'Window':window}
        self.calc_aroon(window)
        self.val = {'Aroon-Up':self.up, 'Aroon-Down':self.down, 'Oscillator':self.osc}
        
    
    def calc_aroon(self, window):
    
        self.up = (100 * self.high.rolling(window).apply(lambda x: x.argmax() + 1) / window) [window-1:]
        self.down = (100 * self.low.rolling(window).apply(lambda x: x.argmin() + 1) / window) [window-1:]
        self.osc = self.up - self.down
    
    
    
class StochOsc(TechIndicator):

    """ stoch(window=14, smawind=3, smoothwind=1)
    
    %K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
    %D = 3-day SMA of %K
    
    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period 
    
    Returns {'pct_k' : 'pct_d'} """
    
    
    def __init__(self, window=14, smoothwind=1, smawind=3, close=None, high=None, low=None):
    
        super().__init__(close=close, high=high, low=low)
        
        self.name = self.stoch_name
        self.parameters = {'%K Window':window, '%D Window':smawind, '%K Smoothing Window':smoothwind}
        self.calc_stoch(window, smawind, smoothwind)
        self.val = {'pct_k' : self.pct_k, 'pct_d' : self.pct_d}
        
    
    def calc_ma(self, window, close):
    
        return MovAvg(window, ma='sma', close=close).ma
    

    def calc_stoch(self, window, smawind, smoothwind):

        temp = (self.close - self.low.rolling(window).min()) / (self.high.rolling(window).max() - self.low.rolling(window).min()) * 100
        self.pct_k = self.calc_ma(smoothwind, temp)
        self.pct_d = self.calc_ma(smawind, self.pct_k)