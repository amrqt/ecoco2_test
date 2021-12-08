from datetime import datetime
import json

import pandas as pd
import numpy as np
import requests


#  start_date = datetime(2017, 1, 1, 0, 0).timestamp()
#  end_date = datetime(2018, 12, 31, 23, 59).timestamp()
# url = 'http://api-recrutement.ecoco2.com/v1/data/?start={}&end={}'.format(start_date, end_date)

# resp = requests.get(url)

file = '/home/axel/Code/ecoco2_test/co2data.json'

# Obtain source data
source_df = pd.io.json.read_json(file).set_index('datetime')

# Create a copy from source data, remove values for half hour rows
interpolated_df = source_df.copy()
interpolated_df[interpolated_df.index.minute == 30] = np.nan

# Fill missing data with linear interpolation
interpolated_df = interpolated_df.interpolate()

# Compute means for weekdays and weekends for source and interpolated data
source_weekday_mean = source_df[source_df.index.weekday < 5].co2_rate.mean()
source_weekend_mean = source_df[source_df.index.weekday >= 5].co2_rate.mean()
interpolated_weekday_mean = interpolated_df[interpolated_df.index.weekday < 5].co2_rate.mean()
interpolated_weekend_mean = interpolated_df[interpolated_df.index.weekday >= 5].co2_rate.mean()

# Join entire source and interpolated data for graph display
graph_df = source_df.join(interpolated_df, rsuffix='_interpolated')

# For the last 20 rows, join source data with interpolated
output_df = graph_df.tail(20).copy()

# Add a column for the difference between interpolated data and source data, apply only to interpolated rows
output_df['difference'] = output_df.apply(
    lambda df: df.co2_rate_interpolated - df.co2_rate if df.name.minute == 30 else '',
    axis=1)

# Add weekday and weekend means for entire dataset
output_df = output_df.append(pd.Series({'co2_rate': source_weekday_mean, 'co2_rate_interpolated': interpolated_weekday_mean, 'difference': ''}, name='Weekday mean'))
output_df = output_df.append(pd.Series({'co2_rate': source_weekend_mean, 'co2_rate_interpolated': interpolated_weekend_mean, 'difference': ''}, name='Weekend mean'))
