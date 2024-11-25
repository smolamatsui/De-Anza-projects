import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class CSVFileReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataframe = None

    def read_csv(self):
        self.dataframe = pd.read_csv(self.filepath)

    def get_dataframe(self):
        if self.dataframe is None:
            raise ValueError("Error: Read the CSV file first")
        return self.dataframe
    
class GraphPlot:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot_data(self, x_col, y_col, title='Change in carbon Emissions by year (1959 - 2019)', xlabel='Y‎ear', ylabel='Average Carbon Emissions (Million Metric Tons)'):
        # I added the ‎, since the y and e in year are pushed together without it
        plt.figure(figsize=(10, 5))
        plt.plot(self.dataframe[x_col], self.dataframe[y_col], marker='o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

class DataProcessor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def filter_data(self):
        filtered_df = self.dataframe[self.dataframe['average'] >= 0]
        return filtered_df

    def calculate_annual_average(self, dataframe):
        annual_data = dataframe.groupby('year')['average'].apply(lambda x: np.mean(x)).reset_index()
        return annual_data


reader = CSVFileReader('Carbon.csv')
reader.read_csv()
df = reader.get_dataframe()
processor = DataProcessor(df)
filtered_data = processor.filter_data()
annual_data = processor.calculate_annual_average(filtered_data)
plotter = GraphPlot(annual_data)
plotter.plot_data(x_col='year', y_col='average')
