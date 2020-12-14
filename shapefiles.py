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

#Define functions
### Great Circle Distance #1: Spherical Law of Cosines
def gc1_sloc(coordinate_1,coordinate_2,radius):
    lon1,lat1 = coordinate_1
    lon2,lat2 = coordinate_2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sin(latrat1)*math.sin(latrat2) + math.cos(latrat1)*math.cos(latrat2)*math.cos(difflonrat)
    cent_ang = math.acos(inner_cent_ang)
    dist_sloc = radius*cent_ang
    return round(dist_sloc,2)

### Great Circle Distance #2: Haversine Formula
def gc2_hf(coord1,coord2,radius):
    lon1,lat1 = coord1
    lon2,lat2 = coord2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sqrt((math.sin(difflatrat/2)**2)+math.cos(latrat1)*math.cos(latrat2)*(math.sin(difflonrat/2)**2))
    cent_ang = 2*math.asin(inner_cent_ang)
    dist_hav = radius*cent_ang
    return round(dist_hav,2)

###Return coordinates
def coord_lister(geom):
    coords = list(geom.coords)
    return (coords)

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Projects')

# LOAD SHAPEFILE
shapefile_path = os.path.join(cd,r'aa_replication',r'gz_2010_us_050_00_500k',r'gz_2010_us_050_00_500k.shp')
county_map = gpd.read_file(shapefile_path)
print(county_map.crs)
county_map = county_map.to_crs("EPSG:4326")
print(county_map.crs)
county_map = county_map[(county_map['STATE'] != '02') & (county_map['STATE'] != '15') & (county_map['STATE'] != '72')]
county_map['geometry'] = county_map['geometry'].buffer(0.0001)
county_map['fips'] = county_map['STATE'] + county_map['COUNTY']


#LOAD FIPS TO CFS MAPPING
crosswalk_path = os.path.join(cd,r'aa_replication',r'cfs-area-lookup-2007-and-2012.xlsx')
crosswalk_xls = pd.ExcelFile(crosswalk_path,engine='openpyxl')
crosswalk_xls_sheet_names = crosswalk_xls.sheet_names
crosswalk = crosswalk_xls.parse(crosswalk_xls_sheet_names[1])
crosswalk = crosswalk[['ANSI ST','ANSI CNTY','CFS07_AREA']]
##make fips codes
crosswalk['ANSI ST'] = crosswalk['ANSI ST'].apply(str)
crosswalk['ANSI ST'] = crosswalk['ANSI ST'].str.zfill(2)
crosswalk['ANSI CNTY'] = crosswalk['ANSI CNTY'].apply(str)
crosswalk['ANSI CNTY'] = crosswalk['ANSI CNTY'].str.zfill(3)
crosswalk['fips'] = crosswalk['ANSI ST'] + crosswalk['ANSI CNTY']
crosswalk['CFS07_AREA'] = crosswalk['CFS07_AREA'].apply(str)
crosswalk.loc[(crosswalk['CFS07_AREA'] == '99999'), 'CFS07_AREA'] = crosswalk['ANSI ST'] + crosswalk['CFS07_AREA'] 
crosswalk = crosswalk[['fips','CFS07_AREA']]
crosswalk.columns = ['fips', 'cfs_area']

##join county map and cfs crosswalk
comb_df = pd.merge(county_map,crosswalk,on='fips',how='inner')
cfs_map = comb_df.dissolve(by='cfs_area')


#projection = "+proj=laea +lat_0=30 +lon_0=-95"
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cmap = plt.get_cmap('plasma')
#cfs_map = cfs_map.to_crs(projection)
cfs_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.show()

cfs_centroids_df = cfs_map[['geometry']].copy()
cfs_centroids_df.geometry = cfs_centroids_df.centroid
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cfs_centroids_df.plot(ax=ax, marker='*', color='red', markersize=1)
cfs_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.show()


#Distances
coordinates = cfs_centroids_df.geometry.apply(coord_lister)
#product('ABCD', repeat=2)
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
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option("display.max_rows", 10, "display.max_columns", 10)
'''
