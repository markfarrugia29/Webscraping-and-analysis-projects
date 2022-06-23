# Credit to Ken Jee for the follow along: https://youtu.be/7O4dpR9QMIM
# Generated 6/22/22 by Mark A. Farrugia

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = r"C:\Users\Tineash\Projects\Glassdoor_webscraper\Data\DA_data_cleaned.csv"
df = pd.read_csv(path)

df.columns

df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Converted Salary', 'City', 'State', 'Company Age (years)']]