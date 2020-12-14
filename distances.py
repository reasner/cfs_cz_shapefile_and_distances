import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#import math
from gcd import gc2_hf
import warnings

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Projects',r'cfs_cz_shapefile_and_distances')
if not os.path.exists(os.path.join(cd,r'cfs07')):
    os.makedirs(os.path.join(cd,r'cfs07'))
if not os.path.exists(os.path.join(cd,r'cz00')):
    os.makedirs(os.path.join(cd,r'cz00'))
cfs_shapfile_path = os.path.join(cd,r'cfs07','cfs07.shp')
cz_shapfile_path = os.path.join(cd,r'cz00','cz00.shp')

# CENTROIDS
##load cfs
cfs_map = gpd.read_file(cfs_shapfile_path)
cfs_centroids_df = cfs_map[['geometry']].copy()
##load cz
cz_map = gpd.read_file(cz_shapfile_path)
cz_centroids_df = cz_map[['geometry']].copy()
##find centroids
warnings.filterwarnings("ignore")
###cfs
cfs_centroids_df.geometry = cfs_centroids_df.centroid
cfs_lon = cfs_centroids_df.centroid.x.tolist()
cfs_lat = cfs_centroids_df.centroid.y.tolist()
##cz
cz_centroids_df.geometry = cz_centroids_df.centroid
cz_lon = cz_centroids_df.centroid.x.tolist()
cz_lat = cz_centroids_df.centroid.y.tolist()
warnings.filterwarnings("default")

# DISTANCES
##cfs
cfs_codes = cfs_map['cfs_area'].tolist()
cfs_areas = list(zip(cfs_lon,cfs_lat))
wgs_mer = 6371000*0.000621371
cfs_distances = []
for ind1,cfs1 in enumerate(cfs_areas):
    for ind2,cfs2 in enumerate(cfs_areas):
        dist = gc2_hf(cfs1,cfs2,wgs_mer)
        orig_cfs_code = cfs_codes[ind1]
        dest_cfs_code = cfs_codes[ind2]
        local_list = [cfs1,cfs2,dist,orig_cfs_code,dest_cfs_code]
        cfs_distances.append(local_list)
orig_cfs_lon = []
orig_cfs_lat = []
dest_cfs_lon = []
dest_cfs_lat = []
dist_cfs = []
orig_cfs_code = []
dest_cfs_code = []
for entry in cfs_distances:
    orig_cfs_lon.append(entry[0][0])
    orig_cfs_lat.append(entry[0][1])
    dest_cfs_lon.append(entry[1][0])
    dest_cfs_lat.append(entry[1][1])
    dist_cfs.append(entry[2])
    orig_cfs_code.append(entry[3])
    dest_cfs_code.append(entry[4])
cfs_out = {'orig_lon':orig_cfs_lon,'orig_lat':orig_cfs_lat,'dest_lon':dest_cfs_lon,'dest_lat':dest_cfs_lat,'dist':dist_cfs,'orig_code':orig_cfs_code,'dest_code':dest_cfs_code}  
cfs_out_df = pd.DataFrame(cfs_out)
cfs_out_path = os.path.join(cd,'cfs07',r'cfs_dist.csv')
cfs_out_df.to_csv(cfs_out_path,index=False)


##cz
cz_codes = cz_map['cz_area'].tolist()
cz_areas = list(zip(cz_lon,cz_lat))
cz_distances = []
for ind1,cz1 in enumerate(cz_areas):
    for ind2,cz2 in enumerate(cz_areas):
        dist = gc2_hf(cz1,cz2,wgs_mer)
        orig_cz_code = cz_codes[ind1]
        dest_cz_code = cz_codes[ind2]
        local_list = [cz1,cz2,dist,orig_cz_code,dest_cz_code]
        cz_distances.append(local_list)
orig_cz_lon = []
orig_cz_lat = []
dest_cz_lon = []
dest_cz_lat = []
dist_cz = []
orig_cz_code = []
dest_cz_code = []
for entry in cz_distances:
    orig_cz_lon.append(entry[0][0])
    orig_cz_lat.append(entry[0][1])
    dest_cz_lon.append(entry[1][0])
    dest_cz_lat.append(entry[1][1])
    dist_cz.append(entry[2])
    orig_cz_code.append(entry[3])
    dest_cz_code.append(entry[4])
cz_out = {'orig_lon':orig_cz_lon,'orig_lat':orig_cz_lat,'dest_lon':dest_cz_lon,'dest_lat':dest_cz_lat,'dist':dist_cz,'orig_code':orig_cz_code,'dest_code':dest_cz_code}  
cz_out_df = pd.DataFrame(cz_out)
cz_out_path = os.path.join(cd,'cz00',r'cz_dist.csv')
cz_out_df.to_csv(cz_out_path,index=False)




