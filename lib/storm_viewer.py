# basics
import os
import os.path as op

# arrays
import numpy as np
import pandas as pd
import xarray as xr
from datetime import date

# matplotlib
from matplotlib import pyplot as plt
from matplotlib import gridspec, animation
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches

# ipywidgets
import ipywidgets as widgets
from ipywidgets import interactive, fixed

# cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# config
import warnings
warnings.simplefilter("ignore")

# custom cmap for the temperature
colorp = ListedColormap(['dimgrey', 'darkgrey','lightgrey','darkorchid',
                         'purple','midnightblue','blue','royalblue','cyan',
                         'turquoise','green','olive','darkkhaki','gold',
                         'darkorange','orangered','red','deeppink','violet',
                         'lightpink'])

def load_cyclons(cyclons_path):
    '''
    This simple function loads the history of cyclons and then allows the
    user to choose between all the different storms available

    Parameters
    ----------
    cyclons_path : str
        This is the path where the cyclons are located. 
        The default is '../resources/storms/TCs_1981_2020.nc'

    Returns
    -------
    tcs : xarray Dataset
        The Dataset where all the cyclons are saved

    '''
    
    # we first load the cyclons and parse the names of them
    print('\n Loading the TCs dataset... \n')
    tcs = xr.open_dataset(cyclons_path)
    tcs['name'] = tcs.name.astype(str)
    
    return tcs

def load_data(tc, # cyclon filtered
              files_path,
              cyclon_area: list = [-20, 185, 20, 30]):
    '''
    This function is very important, as it loads and filters all the
    necessary data to plot the storm behaviour. This, with the previosuly
    cropped tcs xarray dataset (this is done in the jupyter notebook),
    allows the user to plot every cyclon

    Parameters
    ----------
    tc : xarray Dataset
        This is the xarray dataset returned from the widgets section
    files_path : str
        This is the path where all the files are located. 
        The default is '../resources/storms/'
    cyclon_area : list∫
        Area where the cyclon will be plotted and the datasets cropped. 
        The default is [-20, 185, 20, 30] == [lat, lon, dlat, dlon]

    Returns
    -------
    tc : cyclon (singular) dataset
    temp : temperature dataset
    pres : pressure dataset
    mjo : madden julian oscillation dataset
    awt : annual weather type dataset
    precip : maxima monthly precipitation line
    
    All the datasets are 3H interpolated if possible

    '''    
    
    lon_min, lon_max, lat_min, lat_max = tc.lon.min()-5, tc.lon.max()+5, tc.lat.min()-5, tc.lat.max()+5
    
    # we load all the data here
    #print('\n We will now load all the neccessary datasets: \n')
    
    print('\n Loading the track of the cyclon of interest... ')
    tc = tc.isel(storm=0)
   
    tc['time'] = tc['time'].dt.round('s') # round to seconds
    tc = tc.isel(date_time=slice(0,len(tc.time.dropna('date_time').values)))
    
    # change longitude coord values if necessary
    if list(np.where(tc.lon<0)[0]): 
        new_lons = np.where(tc.lon.values>0, tc.lon.values, tc.lon.values+360)
        tc = tc.assign_coords({'lon': new_lons})
    
    print('\n Loading the temperature and the sea level pressure... ')
    temp = xr.open_dataset(op.join(files_path, 'SST_1981_2020.nc'), engine='netcdf4')
    temp = temp.sel(lon=slice(lon_min, lon_max),
                    lat=slice(lat_min, lat_max),
                    time=slice(tc.time.min(),tc.time.max()))
    temp = temp.resample(time='3h').interpolate('nearest')
    pres = xr.open_dataset(op.join(files_path, 'SLPS_1979_2019.nc'), engine='netcdf4').sortby('latitude')
    pres = pres.assign({'SLP': (pres.SLP/100)}) # milibars
    pres = pres.sel(longitude=slice(lon_min, lon_max),
                    latitude=slice(lat_min, lat_max),
                    time=slice(tc.time.min(),tc.time.max()))

    print('\n Loading the MJO files... ')
    mjo = xr.open_dataset(op.join(files_path, 'MJO_1979_2020.nc'), engine='netcdf4')
    mjo = mjo.resample(time='3h').pad()
    mjo = mjo.sel(time=slice(tc.time.min(),tc.time.max()))

    print('\n Loading the AWT... ')
    awt = xr.open_dataset(op.join(files_path, 'AWT_1981_2019.nc'), engine='netcdf4')
    #awt = awt.resample(time='3h').interpolate('nearest')
    awt = awt.sel(time=slice(tc.time.min(),tc.time.max()))

    print('\n Loading the maximum precipitation line... ')
    precip = xr.open_dataset(op.join(files_path, 'MPMC_1979_2020.nc'), engine='netcdf4')

    print('\n All data has been loaded and saved \n')
    
    return (tc, temp, pres, mjo, awt, precip)

def get_category(ycpres):
    'Defines storm category according to minimum pressure centers'
    categ = []
    for i in range(len(ycpres)):
        if (ycpres[i] == 0) or (np.isnan(ycpres[i])):
            categ.append(6)
        elif ycpres[i] < 920:  categ.append(5)
        elif ycpres[i] < 944:  categ.append(4)
        elif ycpres[i] < 964:  categ.append(3)
        elif ycpres[i] < 979:  categ.append(2)
        elif ycpres[i] < 1000: categ.append(1)
        elif ycpres[i] >= 1000: categ.append(0)
    return categ

def get_storm_color(categ):
    'Defines each point of the storm color according to its category'
    colors = []
    for i in range(len(categ)):
        if (categ[i] == 6): colors.append('None')
        elif (categ[i] == 0):  colors.append('green')
        elif (categ[i] == 1):  colors.append('yellow')
        elif (categ[i] == 2):  colors.append('orange')
        elif (categ[i] == 3):  colors.append('red')
        elif (categ[i] == 4): colors.append('purple')
        elif (categ[i] == 5): colors.append('black')
    return colors

def get_edge_color(catcol):
    'Defines markers edge color of each point of the storm'
    colors = []
    for i in range(len(catcol)):
        if (catcol[i] == 'None'): colors.append('None')
        else:  colors.append('black')      
    return colors

#cmap for the temperature
colorp = ListedColormap(["dimgrey", "darkgrey","lightgrey","darkorchid","purple","midnightblue","blue",
                         "royalblue","cyan","turquoise","green","olive","darkkhaki","gold","darkorange","orangered",
                         "red","deeppink","violet","lightpink"])

def get_max_cat(categ):
    'maximum category to print'
    real_cat = []
    for i in range(len(categ)):
        if (categ[i] == 6): real_cat.append(0)
        elif (categ[i] == 0):  real_cat.append(0)
        elif (categ[i] == 1):  real_cat.append(1)
        elif (categ[i] == 2):  real_cat.append(2)
        elif (categ[i] == 3):  real_cat.append(3)
        elif (categ[i] == 4): real_cat.append(4)
        elif (categ[i] == 5): real_cat.append(5)
    return real_cat

def animate(tc, temp, pres, precip, nframes, tinterval,
            figsize=(None,None)): 
    
    # next select lon and lat according to cyclon_area
    lon_min, lon_max, lat_min, lat_max = tc.lon.min()-10, tc.lon.max()+10, tc.lat.min()-10, tc.lat.max()+10
    
    # storm pressure vector
    ptc = tc.wmo_pres
    
    # storm category
    cat = get_category(ptc)
    
    # storm color
    col_cat = get_storm_color(cat)
    
    # marker's edge color
    col_edge = get_edge_color(col_cat)
    
    # maximum category
    real_cat = get_max_cat(cat)
    cat_title = max(real_cat)
    
    # get a handle on the figure and the axes
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))

    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='auto', color='k')
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.gridlines(color='lightgrey', linestyle='-', draw_labels=True)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # place a text box in upper left in axes coords
    text = ('Storm {0}\n Category {1}\n Time: {2}'.format(str(tc.name.values), str(cat_title), str(temp.coords['time'].values[0])[:13]))
    ax.set_title(text, weight='bold')
      
    # initiate contour lines
    contour_opts = {}

    # initialize temperature
    global tmp
    tmp = ax.contourf(
        temp.lon, 
        temp.lat, 
        temp.sst[0,:,:].values.reshape(len(temp.lat),len(temp.lon)), np.arange(10,32,0.5),
        cmap=colorp, alpha=0.5, vmin=22, vmax=32, 
        transform=ccrs.PlateCarree()
                     )
    
    # temperature colorbar
    m = plt.cm.ScalarMappable(cmap=colorp)
    m.set_array(temp.sst[0,:,:])
    c2 = fig.colorbar(m, boundaries=np.arange(22,32,0.5),
                      label='Temperature [ºC]',
                      orientation='vertical', alpha=0.5)
        
    # initialize pressure
    global CS
    CS = ax.contour(
        pres.longitude, 
        pres.latitude, 
        pres.SLP[0,:,:], 60, 
        colors='dimgray', transform=ccrs.PlateCarree()
    )
                   
    # initialize storm
    x = tc.lon
    y = tc.lat
    line , = ax.plot(x, y, color='k', linewidth=4, transform=ccrs.PlateCarree())
    
    # initialize precipitation line
    YY = pd.DatetimeIndex(temp.time.values).year
    MM = pd.DatetimeIndex(temp.time.values).month
     
    years = pd.DatetimeIndex(precip.time.values).year
    months = pd.DatetimeIndex(precip.time.values).month
        
    ind = np.where((years==YY[0])&(months==MM[0]))
    lats = precip.spcz.values[ind[0][0],:]
         
    def draw(frame):
        
        # animate isobars
        global CS
        for tp in CS.collections: tp.remove() # remove the existing contours
                       
        # animate text with the time 
        text = ('Storm {0}\n Category {1}\n Time: {2}'.format(str(tc.name.values), str(cat_title), str(temp.coords['time'].values[frame])[:13]))

        ax.set_title(text)
        
        # animate temperature
        global tmp
        for c in tmp.collections: c.remove() 
        
        tmp = ax.contourf(
            temp.lon, 
            temp.lat, 
            temp.sst[frame,:,:].values.reshape(len(temp.lat), len(temp.lon)), 
            np.arange(10,32,1), 
            alpha=0.5, cmap=colorp, vmin=22, vmax=32, transform=ccrs.PlateCarree()
        )

        # animate pressure in the map
        CS = ax.contour(
            pres.longitude, 
            pres.latitude, 
            pres.SLP[frame,:,:], 
            60, colors='darkgrey', transform=ccrs.PlateCarree(), zorder=1,
        )
        
        ln = ax.plot(x[frame], y[frame], 'o-', color=col_cat[frame],
                       markersize=10, markeredgecolor=col_edge[frame], 
                       markeredgewidth=1.2, transform=ccrs.PlateCarree(), zorder=2)
        
        return (ax)
    
    # Finally, we use the animation module to create the animation
    ani = animation.FuncAnimation(
        fig,                 # figure
        draw,                # name of the function above
        frames=np.arange(0, len(tc.date_time)-5, 5),      # number of frames, starting at 0
        interval=tinterval,  # ms between frames
        repeat=False,
        blit=False,
        save_count=0
    )

    plt.close() # close 
    
    return (ani, fig)

