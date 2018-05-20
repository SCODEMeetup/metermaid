import pandas as pd
# import geopandas as gpd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap, figure

#output_file("toolbar.html")
output_file("c:/users/tony/desktop/workspace/parkingapp/toolbar.html")


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

key = 'API KEY'

# Center on the grid
meter_map_options = GMapOptions(lat=parking_meters.get('Y').mean(),
                                lng=parking_meters.get('X').mean(),
                                map_type="roadmap",
                                zoom=15
                               )

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

meter_map = gmap(google_api_key=key, map_options=meter_map_options, plot_width=500, plot_height=500, title="", tools=[hover])
searching_map = gmap(google_api_key=key, map_options=searching_map_options, title="", tools=[hover])

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
        lat = searching_for_parking.get("AvgLatitude"),
        lon = searching_for_parking.get("AvgLongitude")
    )
)




# Put circles on the map with all of the meter locations
meter_map.circle(x="lon",
                 y="lat",
                 size=5,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source,
                )

meter_map.circle(x="lon",
                 y="lat",
                 size=10,
                 fill_color="red",
                 fill_alpha=0.8,
                 source=searching_source,)

show(meter_map)



