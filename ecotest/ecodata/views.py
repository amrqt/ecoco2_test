
from datetime import datetime

import pandas as pd
import numpy as np
from django.shortcuts import HttpResponse

from ecotest.ecodata.models import CO2DataModel

def CO2TableView(request):
    """ Simple view to render data from a Pandas DataFrame
    """
    co2data = CO2DataModel.objects.get(pk=1).data

    source_df = pd.DataFrame.from_dict(co2data)
    source_df['datetime'] = pd.to_datetime(source_df.datetime)
    source_df = source_df.set_index('datetime')

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

    # For the last 20 rows, join source data with interpolated
    output_df = source_df.tail(20).join(interpolated_df.tail(20), rsuffix='_interpolated')

    # Add a column for the difference between interpolated data and source data, apply only to interpolated rows
    output_df['difference'] = output_df.apply(
        lambda df: df.co2_rate_interpolated - df.co2_rate if df.name.minute == 30 else '',
        axis=1)

    # Add weekday and weekend means for entire dataset
    output_df = output_df.append(pd.Series({'co2_rate': source_weekday_mean, 'co2_rate_interpolated': interpolated_weekday_mean, 'difference': ''}, name='Weekday mean'))
    output_df = output_df.append(pd.Series({'co2_rate': source_weekend_mean, 'co2_rate_interpolated': interpolated_weekend_mean, 'difference': ''}, name='Weekend mean'))

    return HttpResponse(output_df.to_html())