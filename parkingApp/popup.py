from os import environ
import pandas as pd
# import geopandas as gpd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap, figure

parking_meters_csv_file = 'Parking_Meters.csv'
searching_for_parking_csv_file = 'urbaninfrastructure_searchingforparking_csv_searchingforparking.csv'

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

if 'gmaps_api_key' in environ.keys():
    key = environ['gmaps_api_key']
else:
    print("Error please set the gmaps_api_key environment variable so google maps api works")
    exit(1)

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

# hourly_distributions = searching_for_parking.get(["ParkingGeohash", "HourlyDistribution"])

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

hover = HoverTool(tooltips=[
    # ("x, y", "@lat, @lon"),
    ("Meter Number", "@meter_info"),
    ("Location", "@location"),
    ("Side of street", "@side_of_street"),
    ("Blockface", "@blockface"),
    ("Meter Status", "@meter_status"),
    ("Rate", "@rate"),
])

meter_map = gmap(google_api_key=key, map_options=meter_map_options, plot_width=500, plot_height=500, title="Columbus", tools=[hover, 'pan', 'wheel_zoom', 'zoom_in', 'zoom_out'])

# Put circles on the map with all of the meter locations
meter_map.circle(x="lat",
                 y="lon",
                 size=5,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source,
                )

meter_map.circle(x="lat",
                 y="lon",
                 size=10,
                 fill_color="red",
                 fill_alpha=0.8,
                 source=searching_source)

show(meter_map)

