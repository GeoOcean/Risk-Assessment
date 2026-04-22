# basics
import sys
import os
import os.path as op

# arrays

import glob
import wget
import requests

# arrays
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from datetime import date

# config
import warnings
warnings.simplefilter("ignore")

# Ddviewer
def download_ioc_stations(region):
    '''
    Get a list of available stations inside selected region.

    Parameters
    ----------
    region : list
        This is the region where the data wants to be shown
    '''

    url_base = 'http://www.ioc-sealevelmonitoring.org/list.php?operator=&showall=a&output=contacts#'

    # load and correct the stations file
    stations = pd.read_html(url_base)[6].iloc[1:,:8]
    stations.columns = stations.iloc[0,:]
    stations = stations.iloc[1:,:]
    stations = stations.astype(str).astype({'Lat': float, 'Lon': float})

    stations.Lon.where(
        stations.Lon>0, stations.Lon+360, 
        inplace=True
    )
    stations = stations.where(
        (stations.Lon < (region[1] + region[3])) & \
        (stations.Lon > (region[1] - region[3])) & \
        (stations.Lat < (region[0] + region[2])) & \
        (stations.Lat > (region[0] - region[2]))).dropna()

    return stations
    
def download_station_by_code(
    code: str = None,
    time_period: str = '1 week'):
    '''
    This function loads the data from the url indicated, and converts the
    html table to a pandas dataframe, example url (7 days in Tonga):
        - http://www.ioc-sealevelmonitoring.org/
          bgraph.php?code=nkfa&output=tab&period=7
    All the data is in this website:
        - http://www.ioc-sealevelmonitoring.org/
          list.php?showall=a&output=general&order=country&dir=asc

    Parameters
    ----------
    code : str
        station code
    time_period : str
        This is the time period to be downloaded. The default is '1 week',
        but options are: ['12 hours', '1 day', '1 week', '1 month']

    Returns
    -------
    sealevel: pandas DataFrame
        pandas DataFrame with the time and the sea water level

    '''

    # time periods available
    time_periods = {
        '12 hours': '0.5',
        '1 day': '1',
        '1 week': '7',
        '1 month': '30'
    }

    # time period choosed
    time_period = time_periods[time_period]

    # create the url
    url_1 = 'http://www.ioc-sealevelmonitoring.org/bgraph.php?code='
    url_2 = '&output=tab&period='
    url = '{0}{1}{2}{3}'.format(url_1, code, url_2, time_period)

    # download the sealevel
    try:
        print('Downloading data from:\n{0}'.format(url))

        data = pd.read_html(url, header=0)[0]
        data = data.set_index(
            pd.to_datetime(data['Time (UTC)'])).drop(
                columns=['Time (UTC)']
            )
    except:
        print('station data could not be downloaded.')

    return data

# Extremes
def pot(data, th, ie):
    '''
    data:
    th: threshold
    ie: interdenpendy
    '''
    
    # Calculate data over threshold
    data_pot = data.loc[data.values >= th]

    # Days between consecutive events
    ix_space = np.diff(data_pot.index).astype('timedelta64[h]').astype(int)
    ix_space = list(ix_space) + [ie] # include last event

    # Get independent peaks
    idx = []
    for nt in np.where(ix_space)[0]:
        day = data_pot.index[nt]
        rangeday = np.arange(day-datetime.timedelta(days=ie), day+datetime.timedelta(days=ie), datetime.timedelta(hours=1))
        inter, ind1, ind2 = np.intersect1d(data.index, rangeday, return_indices=True)
        if data_pot.iloc[nt].values == np.max(data.iloc[ind1].values):
            idx.append(nt)

    data_pot = data_pot.iloc[idx]

    return(data_pot)