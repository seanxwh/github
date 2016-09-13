
import os
import numpy as np
import pandas as pd
import matpolotlib.pyplot as plt
from math import *

def symbolToPath(symbol, base_dir = 'data'):
    return os.path.join(baseDir, "{}.csv".format(str(symbol)))

# side effects
def fillMissingData(dataFrame):
    methods = ["ffill", "bfill"]
    for mtd in methods: dataFrame.fillna(method = mtd, inplace = True)

def readCSV(symbol):
    csv = symbolToPath(symbol)
    read_csv =  pd.read_csv(
                    csv, index_col = "Date",
                    parse_dates = True, usecols = ["Date", "Adj Close"],
                    na_values = ["nan"])
    return read_csv.rename(columns={"Adj Close":symbol})

def joinSymbolWithDataFrame(symbol, df):
    csv = readCSV(symbol)
    return df.join(csv, how = "inner")

def getData(symbols, dates):
    data_frame_dates = pd.DataFrame(index = dates)
    data_frame_dates = reduce(lambda x,y: joinSymbolWithDataFrame(y,x),symbols,data_frame_dates)
    fillMissingData(data_frame_dates)
    return data_frame_dates



def getRollingMean(data_frame, window):
    """Return rolling mean of given values, using specified window size."""
    return data_frame.rolling(window = window).mean()

def getRollingStd(data_frame, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return data_frame.rolling(window = window).std()

def getBollingerBands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd
    return upper_band, lower_band




def computeDailyReturn(data_frame):
    new_data_frame = data_frame/data_frame.shift(1)-1
    new_data_frame.ix[0,:] = 0
    return new_data_frame

def computeSharpeRatio(data_frame, risk_free_frame, sample_frequency = sqrt(252)):
    return sample_frequency * (data_frame.sub(risk_free_frame).mean()) / (data_frame.sub(risk_free_frame).std())

#   side effects
def plotOverLapHistogramFromDataFrame(data_frame, symbols_array, bins = 40):
    new_data_frame = computeDailyReturn(data_frame)
    for symbol in symbols_array: new_data_frame[symbol].hist(bins = bins, label = symbol)
    plt.show()

def plotScatterFromDataFrame(data_frame, [x_elm,y_elm], plot_fit = False, poly_fit_degree = 1):
    new_data_frame = computeDailyReturn(data_frame)
    new_data_frame.plot(kind = "scatter", x = x_elm, y = y_elm)
    if plot_fit:
        beta_x, beta_y = np.polyfit(new_data_frame[x_elm], new_data_frame[y_elm], poly_fit_degree)
        plt.plot(new_data_frame[x_elm], beta_x * new_data_frame[x_elm] + beta_y, "-", color="red")
    plt.show()
