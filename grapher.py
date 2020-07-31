import matplotlib.pyplot as plt
import yfinance as yf
from datetime import *
import dateutil.relativedelta
import datetime
import pandas as pd
import mplcursors
import matplotlib
import matplotlib.dates as mdates
from dateutil import parser
import numpy as np
from pathlib import Path

class mainObj:
    def getData(self, ticker):
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - dateutil.relativedelta.relativedelta(months=4)
        data = yf.download(ticker, pastDate, currentDate)
        return data[["Volume"]]

    def printData(self, data, stock):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            cleanData_print = data.copy()
            cleanData_print.reset_index(level=0, inplace=True)
            print("\n---- {} ----".format(stock))
            print(cleanData_print.to_string(index=False))

    def barGraph(self, data, stock, save):
        data.reset_index(level=0, inplace=True)
        tempList = []
        for x in data['Date']:
            tempList.append(x.date())
        data['goodDate'] = tempList
        data = data.drop('Date', 1)
        data.set_index('goodDate', inplace=True)
        ################
        fig, ax = plt.subplots(figsize=(15, 7))
        data.plot(kind='bar', ax=ax)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        mplcursors.cursor(hover=True)
        ################
        plt.title(stock)

        if save:
            plt.savefig(file_path)
        else:
            plt.show()

    def lineGraph(self, data, stock, save):
        data.reset_index(level=0, inplace=True)
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.plot(data['Date'], data['Volume'])
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        mplcursors.cursor(hover=True)
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - dateutil.relativedelta.relativedelta(months=4)

        plt.title(stock)

        if save:
            plt.savefig(file_path)
        else:
            plt.show()

    def find_anomalies(self, random_data):
        anomalies = []
        random_data_std = np.std(random_data)
        random_data_mean = np.mean(random_data)
        # Set upper and lower limit to 3 standard deviation
        anomaly_cut_off = random_data_std * 4
        lower_limit = random_data_mean - anomaly_cut_off
        upper_limit = random_data_mean + anomaly_cut_off
        # Generate outliers
        for outlier in random_data:
            if outlier > upper_limit or outlier < lower_limit:
                anomalies.append(outlier)
        return anomalies


# setup
main = mainObj()

# open results file (contains stocks from market_scanner.py output)
with open("results.txt", "r") as f:
    results = f.read().splitlines()

# If you just want the plot for a stock of your choice comment out 
# the with-open block above and uncomment the line below

# results = ['AMZN']

save_or_print = input("Do you want to save the {} graphs as images or print them to screen? [S/p]: ".format(len(results)))

if save_or_print.lower() == 'p':
    save = False
else:
    save = True

for stock in results:
    # create Path object so it works for all OS's
    file_path = Path("figures/{}_{}.png".format(stock, datetime.date.today()))

    data = main.getData(stock)
    #main.printData(data, stock, save)
    #main.barGraph(data, stock, save)
    main.lineGraph(data, stock, save)
