import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions,ColorBar, LinearColorMapper, LogColorMapper
from bokeh.plotting import gmap
import numpy as np

from bokeh.layouts import gridplot


csv_file = 'urbaninfrastructure_searchingforparking_csv_searchingforparking.csv'

data = pd.read_csv(csv_file,
            delimiter=',',
            parse_dates=True,
            infer_datetime_format=True,

            )
key = 'AIzaSyDjN80ThEj0GIp49sNk1k3iLTDalMponxg'

lat = data.get('AvgLatitude')
lng = data.get('AvgLongitude')
time = data.get('AvgTimeToPark')

# Center on the grid
map_options = GMapOptions(lat=lat.mean(),
                          lng=lng.mean(),
                          map_type="roadmap",
                          zoom=11)
p = gmap(google_api_key=key, map_options=map_options, title="Columbus?")

source = ColumnDataSource(
    dict(
        lat = lat,
        lon = lng
    )
)
color_mapper = LinearColorMapper(palette='Magma256', low=min()
p.scatter(
p.circle(x="lon",
         y="lat",
         size=5,
         fill_color="blue",
         fill_alpha=0.8,
         source=source)
show(p)
