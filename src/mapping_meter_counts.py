from os import environ
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap

# Need to disable some warnings ;)
# (...snip) pydevd_resolver.py:71: FutureWarning: Series.flags is deprecated and will be removed in a future version
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

###
#
# Spec
#
# 1. Mapping meter count = Parking Meters + Parking transaction data (2015-2017)
#    1. Parking Meters -
#        1. Longitude x/ Latitude y/
#    2. Parking transaction data (2015-2017) -
#        1. Longitude and latitude
#        2. count (meter ids)
#        3. meter_id <inner join> pole
#
###

# for console / programmatic setting
# environ.__setitem__('gmaps_api_key', 'xxxx')
if 'gmaps_api_key' in environ.keys():
    key = environ['gmaps_api_key']
else:
    print("Error please set the gmaps_api_key environment variable so google maps api works")
    exit(1)

parking_meters_csv_file = 'Parking_Meters.csv'
meter_transactions_file = 'parking_meters_data_2015_2017.csv'

# Columns:
# Index(['X', 'Y', 'OBJECTID', 'METER_ID', 'LOCATION', 'SIDE_OF_STREET',
#        'BLOCKFACE', 'METER_STATUS', 'TOW_AWAY_HOURS', 'METER_TIME', 'HANDICAP',
#        'HOURS_OPERATION', 'IN_SERVICE', 'VALET_HOURS', 'RATE',
#        'FOOD_SERVICE_HOURS', 'TAXI_ZONE_HOURS', 'CHARGING_STATION',
#        'CHARGING_STATION_STATUS'],
#       dtype='object')
parking_meters  :pd.DataFrame = pd.read_csv(parking_meters_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )
# Columns:
# Index(['Pole', 'ParkingStartDate', 'ParkingEndDate', 'TransactionType',
#        'TotalCredit'],
#       dtype='object')
meter_transactions :pd.DataFrame = pd.read_csv(meter_transactions_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )

# Create a merged dataset joined by the meter_id and pole columns
merged_df : pd.DataFrame = pd.DataFrame.merge(parking_meters, meter_transactions, how='left', left_on='METER_ID', right_on='Pole')
counts_per_pole :pd.DataFrame = merged_df.where(merged_df['TotalCredit'] != None).groupby('Pole').count()

# The AvgLat and AvgLong are to try to center the chart
# Adjust the zoom value to zoom in/out based on need.
# The value here is only an initial zoom level
meter_map_options = GMapOptions(lat=merged_df.Y.mean(),
                                lng=merged_df.X.mean(),
                                map_type="roadmap",
                                zoom=15)

# This we will want to adjust based on the needs of the spec
meter_source = ColumnDataSource(
    dict(
        lat = merged_df.Y,
        lon = merged_df.X,
        size = counts_per_pole.TotalCredit,
        meter_info=merged_df.METER_ID,
        location=merged_df.LOCATION,
        side_of_street=merged_df.SIDE_OF_STREET,
        blockface=merged_df.BLOCKFACE,
        meter_status=merged_df.METER_STATUS,
        rate=merged_df.RATE,
        total = counts_per_pole.TotalCredit
    )
)

hover = HoverTool(tooltips=[
    # ("x, y", "@lat, @lon"),
    ("Meter Number", "@meter_info"),
    ("Location", "@location"),
    ("Side of street", "@side_of_street"),
    ("Blockface", "@blockface"),
    ("Meter Status", "@meter_status"),
    ("Rate", "@rate"),
    ("Total Spent", "@total"),
])

meter_map = gmap(google_api_key=key, map_options=meter_map_options, title="Columbus", tools=[hover, 'pan', 'wheel_zoom', 'zoom_in', 'zoom_out'])

# Put circles on the map with all of the meter locations. The size of the dot is based on number of transactions
# todo, the original map from Nathan had size/color gradients based on
meter_map.circle(x="lon",
                 y="lat",
                 size="size",
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source)

show(meter_map)
