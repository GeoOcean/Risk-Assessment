import os
import os.path as op
import sys

import plotly.graph_objects as go
import plotly.express as px
from IPython.display import HTML

sys.path.insert(0, op.join(os.getcwd(), '..'))

from lib.config import *

colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']  

def px_databases(df_wnd, df_wvs, df_prec, stations_ioc, stations_bom, codec, df_pres):
    
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(lat=df_wnd['lat'], lon=df_wnd['lon'],
                                   mode='markers', marker=go.scattermapbox.Marker(size=5),
                                   name='Wind CFSR',
                                   text=['ID number: {0}'.format(i) for i in df_wnd.index]))

    fig.add_trace(go.Scattermapbox(lat=df_wvs['lat'], lon=df_wvs['lon'],
                                   mode='markers', marker=go.scattermapbox.Marker(size=5),
                                   name='Waves CSIRO',
                                   text=['ID number: {0}'.format(i) for i in df_wvs.index]))

    fig.add_trace(go.Scattermapbox(lat=df_prec['lat'], lon=df_prec['lon'],
                                   mode='markers', marker=go.scattermapbox.Marker(size=6),
                                   name='Precipitation CFS',
                                   text=['ID number: {0}'.format(i) for i in df_prec.index]))
    
    fig.add_trace(go.Scattermapbox(lat=df_pres['lat'], lon=df_pres['lon'],
                                   mode='markers', marker=go.scattermapbox.Marker(size=6),
                                   name='Pressure CFSR',
                                   text=['ID number: {0}'.format(i) for i in df_pres.index]))

    fig.add_trace(go.Scattermapbox(lat=stations_ioc['Lat'],lon=stations_ioc['Lon'],
                                     mode='markers',marker=go.scattermapbox.Marker(size=9),
                                     name='Sea level IOC',
                                     text=['Code: ' + stations_ioc['Code'].iloc[i] + '<br>' + stations_ioc['Location'].iloc[i] for i in range(stations_ioc.shape[0])]))

    fig.add_trace(go.Scattermapbox(lat=stations_bom.Lat.values,lon=stations_bom.Lon.values,
                                     mode='markers',marker=go.scattermapbox.Marker(size=9),
                                     name='Sea level BOM',
                                     text=['Code: ' + stations_bom['ID_CODE'].values[i] + '<br>' + stations_bom['Country'].values[i] for i in range(len(stations_bom.ID_CODE))]))

    fig.add_trace(go.Scattermapbox(lat=-codec.Lat.values,lon=codec.Lon.values,
                                     mode='markers',marker=go.scattermapbox.Marker(size=8),
                                     name='Storm Surge CODEC',
                                     text=['Code: ' + str(int(codec['Station'].values[i]))  for i in range(len(codec.Station))]))

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.93))
    fig.update_layout(mapbox_style="open-street-map",
                      width=1000,
                      mapbox=dict(
                            bearing=0,
                            center=go.layout.mapbox.Center(
                                lat=region[0],
                                lon=region[1]
                                ),
                            pitch=0,
                            zoom=3
                        ),
                      margin={"r":0,"t":0,"l":0,"b":0},
                      showlegend=True,

                     )

    fig.show()