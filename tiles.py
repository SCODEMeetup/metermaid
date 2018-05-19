import numpy as np
import pandas as pd
# import geopandas as gpd

import Geohash
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap

parking_meters_csv_file = 'Parking_Meters.csv'
searching_for_parking_csv_file = 'urbaninfrastructure_searchingforparking_csv_searchingforparking.csv'

parking_meters = pd.read_csv(parking_meters_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True
            )

searching_for_parking = pd.read_csv(searching_for_parking_csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,
            )


key = 'AIzaSyDjN80ThEj0GIp49sNk1k3iLTDalMponxg'
# Center on the grid
meter_map_options = GMapOptions(lat=parking_meters.get('Y').mean(),
                                lng=parking_meters.get('X').mean(),
                                map_type="roadmap",
                                zoom=15)

searching_map_options = GMapOptions(lat=searching_for_parking.get('AvgLatitude').mean(),
                                lng=searching_for_parking.get('AvgLongitude').mean(),
                                map_type="roadmap",
                                zoom=14)

meter_map = gmap(google_api_key=key, map_options=meter_map_options, title="Columbus")
searching_map = gmap(google_api_key=key, map_options=searching_map_options, title="Columbus")

# decode the geohashes
larger = [i[0:7] for i in searching_for_parking.get("ParkingGeohash")]
tiles = [Geohash.decode(i, delta=True) for i in larger]
#tiles = list(map(Geohash.decode_exactly, searching_for_parking.get("ParkingGeohash")))

meter_source = ColumnDataSource(
    dict(
        lat = parking_meters.get("Y"),
        lon = parking_meters.get("X")
    )
)

searching_source = ColumnDataSource(
    dict(
        y_coords = [[i[0] - i[2], i[0] - i[3], i[0] + i[3], i[0] + i[3]] for i in tiles],
        x_coords = [[i[1] - i[3], i[1] + i[3], i[1] + i[3], i[1] - i[3]] for i in tiles]
    )
)

# Put circles on the map with all of the meter locations
meter_map.rect(x="lon",
                 y="lat",
                 width=50,
                 height=50,
                 fill_color="blue",
                 fill_alpha=0.8,
                 source=meter_source)

searching_map.patches(xs="x_coords",
                    ys="y_coords",
                    fill_color="blue",
                    fill_alpha=0.4,
                    source=searching_source
                )

#show(meter_map)
show(searching_map)
