import pandas as pd
# import geopandas as gpd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap

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

key = 'find_your_api_key'

# Center on the grid
meter_map_options = GMapOptions(lat=parking_meters.get('Y').mean(),
                                lng=parking_meters.get('X').mean(),
                                map_type="roadmap",
                                zoom=15)

searching_map_options = GMapOptions(lat=searching_for_parking.get('AvgLatitude').mean(),
                                lng=searching_for_parking.get('AvgLongitude').mean(),
                                map_type="roadmap",
                                zoom=15)

meter_map = gmap(google_api_key=key, map_options=meter_map_options, title="Columbus")
searching_map = gmap(google_api_key=key, map_options=searching_map_options, title="Columbus")

meter_source = ColumnDataSource(
    dict(
        lat = parking_meters.get("Y"),
        lon = parking_meters.get("X")
    )
)

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
                 source=meter_source)

searching_map.circle(x="lon",
                 y="lat",
                 size=5,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=searching_source)

show(meter_map)
show(searching_map)
