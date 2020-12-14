import urllib
import urllib.request
import os
import shutil
import zipfile
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import itertools
from gcd import gc2_hf

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Projects',r'cfs_cz_shapefile_and_distances')
if not os.path.exists(os.path.join(cd,r'cfs07')):
    os.makedirs(os.path.join(cd,r'cfs07'))

# LOAD COUNTY SHAPEFILE
shapefile_path = os.path.join(cd,r'gz_2010_us_050_00_500k',r'gz_2010_us_050_00_500k.shp')
county_map = gpd.read_file(shapefile_path)
county_map = county_map.to_crs("EPSG:4326")
county_map = county_map[(county_map['STATE'] != '02') & (county_map['STATE'] != '15') & (county_map['STATE'] != '72')]
county_map['geometry'] = county_map['geometry'].buffer(0.0001)
county_map['fips'] = county_map['STATE'] + county_map['COUNTY']


# MAKE CFS SHAPEFILE
crosswalk_path = os.path.join(cd,r'cfs-area-lookup-2007-and-2012.xlsx')
crosswalk_xls = pd.ExcelFile(crosswalk_path,engine='openpyxl')
crosswalk_xls_sheet_names = crosswalk_xls.sheet_names
crosswalk = crosswalk_xls.parse(crosswalk_xls_sheet_names[1])
crosswalk = crosswalk[['ANSI ST','ANSI CNTY','CFS07_AREA','CFS07_NAME']]
##make fips codes
crosswalk['ANSI ST'] = crosswalk['ANSI ST'].apply(str)
crosswalk['ANSI ST'] = crosswalk['ANSI ST'].str.zfill(2)
crosswalk['ANSI CNTY'] = crosswalk['ANSI CNTY'].apply(str)
crosswalk['ANSI CNTY'] = crosswalk['ANSI CNTY'].str.zfill(3)
crosswalk['fips'] = crosswalk['ANSI ST'] + crosswalk['ANSI CNTY']
crosswalk['CFS07_AREA'] = crosswalk['CFS07_AREA'].apply(str)
crosswalk.loc[(crosswalk['CFS07_AREA'] == '99999'), 'CFS07_AREA'] = crosswalk['ANSI ST'] + crosswalk['CFS07_AREA'] 
crosswalk = crosswalk[['fips','CFS07_AREA','CFS07_NAME']]
crosswalk.columns = ['fips', 'cfs_area','cfs_name']
##join county map and cfs crosswalk
comb_df = pd.merge(county_map,crosswalk,on='fips',how='inner')
cfs_map = comb_df.dissolve(by='cfs_area')
cfs_map.reset_index(inplace=True)
cfs_map = cfs_map[['cfs_area','cfs_name','geometry']]
cfs_shapfile_path = os.path.join(cd,r'cfs07','cfs07.shp')
cfs_map.to_file(cfs_shapfile_path,driver='ESRI Shapefile')

# MAKE CZ SHAPEFILE



# TEST NEW SHAPEFILES BY PLOTTING
##cfs shapefile
cfs_reload_map = gpd.read_file(cfs_shapfile_path)
projection = "+proj=laea +lat_0=30 +lon_0=-95"
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cmap = plt.get_cmap('plasma')
cfs_reload_map = cfs_reload_map.to_crs(projection)
cfs_reload_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.show()

##cz shapfile
'''
cfs_centroids_df = cfs_map[['geometry']].copy()
cfs_centroids_df.geometry = cfs_centroids_df.centroid
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cfs_centroids_df.plot(ax=ax, marker='*', color='red', markersize=1)
cfs_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.show()


#Distances
lon = cfs_centroids_df.centroid.x.tolist()
lat = cfs_centroids_df.centroid.y.tolist()
cfs_areas = list(zip(lon, lat))
wgs_mer = 6371000*0.000621371
distances = []
for cfs1 in cfs_areas:
    for cfs2 in cfs_areas:
        dist = gc2_hf(cfs1,cfs2,wgs_mer)
        local_list = [cfs1,cfs2,dist]
        distances.append(local_list)

orig_lon = []
orig_lat = []
dest_lon = []
dest_lat = []
dist = []

for entry in distances:
    orig_lon.append(entry[0][0])
    orig_lat.append(entry[0][1])
    dest_lon.append(entry[1][0])
    dest_lat.append(entry[1][1])
    dist.append(entry[2])

cfs_out = {'orig_lon':orig_lon,'orig_lat':orig_lat,'dest_lon':dest_lon,'dest_lat':dest_lat,'dist':dist}  
cfs_out_df = pd.DataFrame(cfs_out)
cfs_out_path = os.path.join(cd,r'aa_replication',r'cfs_dist.csv')
cfs_out_df.to_csv(cfs_out_path,index=False)
'''

'''
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option("display.max_rows", 10, "display.max_columns", 10)
'''
