from os import environ
import pandas as pd
from pandas.io.json import json_normalize
from json import loads

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap

# Need to disable some warnings ;)
# (...snip) pydevd_resolver.py:71: FutureWarning: Series.flags is deprecated and will be removed in a future version
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

if 'gmaps_api_key' in environ.keys():
    key = environ['gmaps_api_key']
else:
    print("Error please set the gmaps_api_key environment variable so google maps api works")
    exit(1)

parking_meters_csv_file = 'Parking_Meters.csv'
searching_for_parking_csv_file = 'urbaninfrastructure_searchingforparking_csv_searchingforparking.csv'

# Are we going to
parking_meters = pd.read_csv(parking_meters_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )

searching_for_parking = pd.read_csv(searching_for_parking_csv_file,
                                    delimiter=',',
                                    parse_dates=True,
                                    infer_datetime_format=True,
                                    )

# Just get the columns we need
columns = ["ParkingGeohash", "AvgLatitude", "AvgLongitude", "HourlyDistribution", "TotalSearching"]
data = searching_for_parking.filter(columns).copy()

# We need to apply the hourly distribution to the TotalSearching to each entry from HourlyDistribution
# We know the location from locations ParkingGeohash
# For each day
#   for each hour
#     multiply the value of TotalSearching * HourlyDistribution

# hours_values = data.filter(["ParkingGeohash", "HourlyDistribution"]).copy()

# This builds a new dictionary. The key is the ParkingGeohash and the value is the deserialized json of the HourlyDistribution
# The values in the json are {HH: Y.YYY} where HH is the 2-digit hour ( 24 ) and minutes.seconds of search
# hours = dict()
# for row in hours_values.itertuples():
#     hours[row.ParkingGeohash] = loads(row.HourlyDistribution)

# The AvgLat and AvgLong are to try to center the chart
meter_map_options = GMapOptions(lat=parking_meters.get('Y').mean(),
                                lng=parking_meters.get('X').mean(),
                                map_type="roadmap",
                                zoom=15)

# The AvgLat and AvgLong are to try to center the chart
searching_map_options = GMapOptions(lat=searching_for_parking.get('AvgLatitude').mean(),
                                    lng=searching_for_parking.get('AvgLongitude').mean(),
                                    map_type="roadmap",
                                    zoom=15)

hover = HoverTool(tooltips=[
    # ("x, y", "@lat, @lon"),
    ("Meter Number", "@meter_info"),
    ("Location", "@location"),
    ("Side of street", "@side_of_street"),
    ("Blockface", "@blockface"),
    ("Meter Status", "@meter_status"),
    ("Rate", "@rate"),
])

# meter_map = gmap(google_api_key=key, map_options=meter_map_options, title="Columbus")
meter_map = gmap(google_api_key=key, map_options=meter_map_options, plot_width=500, plot_height=500, title="Columbus", tools=[hover, 'pan', 'wheel_zoom', 'zoom_in', 'zoom_out'])
searching_map = gmap(google_api_key=key, map_options=searching_map_options, title="Columbus")

# meter_source = ColumnDataSource(
#     dict(
#         lat = parking_meters.get("Y"),
#         lon = parking_meters.get("X")
#     )
# )

meter_source = ColumnDataSource(
  dict(
       lat = parking_meters.get("Y"),
       lon = parking_meters.get("X"),
       meter_info = parking_meters.get("METER_ID"),
       location = parking_meters.get("LOCATION"),
       side_of_street = parking_meters.get("SIDE_OF_STREET"),
       blockface = parking_meters.get("BLOCKFACE"),
       meter_status = parking_meters.get("METER_STATUS"),
       rate = parking_meters.get("RATE"),
))

searching_source = ColumnDataSource(
    dict(
        lat=searching_for_parking.get("AvgLatitude"),
        lon=searching_for_parking.get("AvgLongitude")
    )
)

# Put circles on the map with all of the meter locations
meter_map.circle(x="lon",
                 y="lat",
                 size=5,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source)

meter_map.circle(x="lon",
                     y="lat",
                     size=5,
                     fill_color="red",
                     fill_alpha=0.8,
                     source=searching_source)

show(meter_map)
# show(searching_map)
