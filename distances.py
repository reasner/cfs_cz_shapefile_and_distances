import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#import math
from gcd import gc2_hf
import warnings

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Dropbox',r'projects',r'cfs_cz_shapefile_and_distances')
if not os.path.exists(os.path.join(cd,r'cfs07')):
    os.makedirs(os.path.join(cd,r'cfs07'))
if not os.path.exists(os.path.join(cd,r'cz00')):
    os.makedirs(os.path.join(cd,r'cz00'))
if not os.path.exists(os.path.join(cd,r'fips')):
    os.makedirs(os.path.join(cd,r'fips'))
if not os.path.exists(os.path.join(cd,r'fips',r'distances')):
    os.makedirs(os.path.join(cd,r'fips',r'distances'))
cfs_shapfile_path = os.path.join(cd,r'cfs07','cfs07.shp')
cz_shapfile_path = os.path.join(cd,r'cz00','cz00.shp')
county_shapfile_path = os.path.join(cd,r'fips','fips.shp')

# CENTROIDS
##load cfs
cfs_map = gpd.read_file(cfs_shapfile_path)
cfs_centroids_df = cfs_map[['geometry']].copy()
##load cz
cz_map = gpd.read_file(cz_shapfile_path)
cz_centroids_df = cz_map[['geometry']].copy()
##load uniform counties
county_map = gpd.read_file(county_shapfile_path)
county_centroids_df = county_map[['geometry']].copy()

##find centroids
'''
If differentiating between land and water costs, it may make sense to use
.representative_point(), which ensures that the "centroid" falls within
the bounds of the area (i.e. not another area and not in a body of water).
However, for a single measure of distance, the centroid seems better given
a comparison of the graphs.
'''
warnings.filterwarnings("ignore")
###cfs
cfs_centroids_df.geometry = cfs_centroids_df.centroid
cfs_lon = cfs_centroids_df.centroid.x.tolist()
cfs_lat = cfs_centroids_df.centroid.y.tolist()
##cz
cz_centroids_df.geometry = cz_centroids_df.centroid
cz_lon = cz_centroids_df.centroid.x.tolist()
cz_lat = cz_centroids_df.centroid.y.tolist()
##counties
county_centroids_df.geometry = county_centroids_df.centroid
county_lon = county_centroids_df.centroid.x.tolist()
county_lat = county_centroids_df.centroid.y.tolist()
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

##county
county_codes = county_map['fips'].tolist()
county_areas = list(zip(county_lon,county_lat))
county_distances = []
for ind1,county1 in enumerate(county_areas):
    for ind2,county2 in enumerate(county_areas):
        dist = gc2_hf(county1,county2,wgs_mer)
        orig_county_code = county_codes[ind1]
        dest_county_code = county_codes[ind2]
        local_list = [county1,county2,dist,orig_county_code,dest_county_code]
        county_distances.append(local_list)
orig_county_lon = []
orig_county_lat = []
dest_county_lon = []
dest_county_lat = []
dist_county = []
orig_county_code = []
dest_county_code = []
for entry in county_distances:
    orig_county_lon.append(entry[0][0])
    orig_county_lat.append(entry[0][1])
    dest_county_lon.append(entry[1][0])
    dest_county_lat.append(entry[1][1])
    dist_county.append(entry[2])
    orig_county_code.append(entry[3])
    dest_county_code.append(entry[4])
county_out = {'orig_lon':orig_county_lon,'orig_lat':orig_county_lat,'dest_lon':dest_county_lon,'dest_lat':dest_county_lat,'dist':dist_county,'orig_code':orig_county_code,'dest_code':dest_county_code}  
county_out_df = pd.DataFrame(county_out)
county_out_path = os.path.join(cd,r'fips',r'distances',r'county_dist.csv')
county_out_df.to_csv(county_out_path,index=False)

# BOUNDS
'''
Needed if interested in normalizing E-W distance to 1 (to align with AA14)
'''
##cfs (min_x, min_y, max_x, max_y)
cfs_min_lon = min(cfs_lon)
cfs_max_lon = max(cfs_lon)
cfs_width = cfs_max_lon - cfs_min_lon
cfs_min_lat = min(cfs_lat)
cfs_max_lat = max(cfs_lat)
cfs_height = cfs_max_lat - cfs_min_lat
cfsb1 = (cfs_max_lon,cfs_min_lat+0.5*cfs_height)
cfsb2 = (cfs_min_lon,cfs_min_lat+0.5*cfs_height)
cfs_width = gc2_hf(cfsb1,cfsb2,wgs_mer)
##cz (min_x, min_y, max_x, max_y)
cz_min_lon = min(cz_lon)
cz_max_lon = max(cz_lon)
cz_width = cz_max_lon - cz_min_lon
cz_min_lat = min(cz_lat)
cz_max_lat = max(cz_lat)
cz_height = cz_max_lat - cz_min_lat
czb1 = (cz_max_lon,cz_min_lat+0.5*cz_height)
czb2 = (cz_min_lon,cz_min_lat+0.5*cz_height)
cz_width = gc2_hf(czb1,czb2,wgs_mer)
##fips (min_x, min_y, max_x, max_y)
county_min_lon = min(county_lon)
county_max_lon = max(county_lon)
county_width = county_max_lon - county_min_lon
county_min_lat = min(county_lat)
county_max_lat = max(county_lat)
county_height = county_max_lat - county_min_lat
countyb1 = (county_max_lon,county_min_lat+0.5*county_height)
countyb2 = (county_min_lon,county_min_lat+0.5*county_height)
county_width = gc2_hf(countyb1,countyb2,wgs_mer)

# NORMALIZED DISTANCES
#cfs
cfs_out_df['dist'] = cfs_out_df['dist']/cfs_width
norm_cfs_out_path = os.path.join(cd,r'cfs07',r'norm_cfs_dist.csv')
cfs_out_df.to_csv(norm_cfs_out_path,index=False)
#cz
cz_out_df['dist'] = cz_out_df['dist']/cz_width
norm_cz_out_path = os.path.join(cd,r'cz00',r'norm_cz_dist.csv')
cz_out_df.to_csv(norm_cz_out_path,index=False)
#fips
county_out_df['dist'] = county_out_df['dist']/county_width
norm_county_out_path = os.path.join(cd,r'fips',r'distances',r'norm_county_dist.csv')
county_out_df.to_csv(norm_county_out_path,index=False)

# PLOTS
##cfs
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cfs_map.plot(ax=ax,facecolor="none",linewidth=0.5, edgecolor='gray')
cfs_centroids_df.plot(ax=ax,marker='*',color='red',markersize=1)
plt.title('CFS (2007) Boundaries and Centroids')
cfs_plot_path = os.path.join(cd,r'cfs07','cfs_cent_plot.png')
plt.savefig(cfs_plot_path,bbox_inches='tight',dpi=300)
##cz
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cz_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
cz_centroids_df.plot(ax=ax,marker='*',color='red',markersize=1)
plt.title('CZ (2007) Boundaries and Centroids')
cz_plot_path = os.path.join(cd,r'cz00','cz_cent_plot.png')
plt.savefig(cz_plot_path,bbox_inches='tight',dpi=300)
##county
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
county_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
county_centroids_df.plot(ax=ax,marker='*',color='red',markersize=1)
plt.title('FIPS (Uniform) Boundaries and Centroids')
county_plot_path = os.path.join(cd,r'fips','county_cent_plot.png')
plt.savefig(county_plot_path,bbox_inches='tight',dpi=300)
