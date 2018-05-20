import pandas as pd
from pandas.io.json import json_normalize
from json import loads

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap

# Need to disable some warnings ;)
# (...snip) pydevd_resolver.py:71: FutureWarning: Series.flags is deprecated and will be removed in a future version
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

###
#
# Spec
#
# Mapping meter count = Parking Meters + Parking transaction data (2015-2017)
# Parking Meters -
# Longitude x/ Latitude y/
# Parking transaction data (2015-2017) -
# Longitude and latitude
# count (meter ids)
# meter_id pole
#
###

key = 'find_your_api_key'
parking_meters_csv_file = 'Parking_Meters.csv'
meter_transactions_file = 'parking_meters_data_2015_2017.csv'

# Are we going to
parking_meters = pd.read_csv(parking_meters_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )
meter_transactions = pd.read_csv(parking_meters_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )


# The AvgLat and AvgLong are to try to center the chart
meter_map_options = GMapOptions(lat=parking_meters.get('Y').mean(),
                                lng=parking_meters.get('X').mean(),
                                map_type="roadmap",
                                zoom=15)


meter_map = gmap(google_api_key=key, map_options=meter_map_options, title="Columbus")

meter_source = ColumnDataSource(
    dict(
        lat = parking_meters.get("Y"),
        lon = parking_meters.get("X")
    )
)

# Put circles on the map with all of the meter locations
meter_map.circle(x="lon",
                 y="lat",
                 size=5,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source)

show(meter_map)
