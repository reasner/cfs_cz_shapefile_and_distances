import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#import math
from gcd import gc2_hf

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Projects',r'cfs_cz_shapefile_and_distances')
if not os.path.exists(os.path.join(cd,r'cfs07')):
    os.makedirs(os.path.join(cd,r'cfs07'))
if not os.path.exists(os.path.join(cd,r'cz00')):
    os.makedirs(os.path.join(cd,r'cz00'))
cfs_shapfile_path = os.path.join(cd,r'cfs07','cfs07.shp')
cz_shapfile_path = os.path.join(cd,r'cz00','cz00.shp')

# CENTROIDS
##cfs
cfs_map = gpd.read_file(cfs_shapfile_path)
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
codes = cfs_map['cfs_area'].tolist()
cfs_areas = list(zip(lon, lat))
wgs_mer = 6371000*0.000621371
distances = []
for ind1,cfs1 in enumerate(cfs_areas):
    for ind2,cfs2 in enumerate(cfs_areas):
        dist = gc2_hf(cfs1,cfs2,wgs_mer)
        orig_code = codes[ind1]
        dest_code = codes[ind2]
        local_list = [cfs1,cfs2,dist,orig_code,dest_code]
        distances.append(local_list)

orig_lon = []
orig_lat = []
dest_lon = []
dest_lat = []
dist = []
orig_code = []
dest_code = []

for entry in distances:
    orig_lon.append(entry[0][0])
    orig_lat.append(entry[0][1])
    dest_lon.append(entry[1][0])
    dest_lat.append(entry[1][1])
    dist.append(entry[2])
    orig_code.append(entry[3])
    dest_code.append(entry[4])

cfs_out = {'orig_lon':orig_lon,'orig_lat':orig_lat,'dest_lon':dest_lon,'dest_lat':dest_lat,'dist':dist,'orig_code':orig_code,'dest_code':dest_code}  
cfs_out_df = pd.DataFrame(cfs_out)
cfs_out_path = os.path.join(cd,'cfs07',r'cfs_dist.csv')
cfs_out_df.to_csv(cfs_out_path,index=False)




