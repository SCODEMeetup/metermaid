import pandas as pd
# import geopandas as gpd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap

csv_file = 'Parking_Meters.csv'

data = pd.read_csv(csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,

            )

key = 'find_your_api_key'

# Center on the grid
map_options = GMapOptions(lat=data.get('X').mean(),
                          lng=data.get('Y').mean(),
                          map_type="roadmap",
                          zoom=11)

p = gmap(google_api_key=key, map_options=map_options, title="Columbus?")

source = ColumnDataSource(
    dict(
        lat = data.get("X"),
        lon = data.get("Y")
    )
)

# Put circles on the map with all of the meter locations
p.circle(x="lon",
         y="lat",
         size=5,
         fill_color="blue",
         fill_alpha=0.8,
         source=source)
