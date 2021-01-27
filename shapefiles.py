import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import warnings

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Documents',r'projects',r'cfs_cz_shapefile_and_distances')
if not os.path.exists(os.path.join(cd,r'cfs07')):
    os.makedirs(os.path.join(cd,r'cfs07'))
if not os.path.exists(os.path.join(cd,r'cz00')):
    os.makedirs(os.path.join(cd,r'cz00'))
if not os.path.exists(os.path.join(cd,r'fips')):
    os.makedirs(os.path.join(cd,r'fips'))

# LOAD COUNTY SHAPEFILE
shapefile_path = os.path.join(cd,r'gz_2010_us_050_00_500k',r'gz_2010_us_050_00_500k.shp')
county_map = gpd.read_file(shapefile_path)
county_map = county_map[(county_map['STATE'] != '02') & (county_map['STATE'] != '15') & (county_map['STATE'] != '72')]
county_map['fips'] = county_map['STATE'] + county_map['COUNTY']
warnings.filterwarnings("ignore")
county_map = county_map.to_crs("EPSG:5070")
county_map['geometry'] = county_map['geometry'].buffer(5)
warnings.filterwarnings("default")

# FIPS Shapefile
fips_crosswalk = pd.read_csv('fips_crosswalk.csv')
fips_crosswalk['fips'] = fips_crosswalk['fips'].apply(str)
fips_crosswalk['fips'] = fips_crosswalk['fips'].str.zfill(5)
fips_crosswalk['new_fips'] = fips_crosswalk['new_fips'].apply(str)
fips_crosswalk['new_fips'] = fips_crosswalk['new_fips'].str.zfill(5)
county_map = county_map[['fips','geometry']]
county_map['year'] = 2000
county_comb_df = pd.merge(county_map,fips_crosswalk,on=['fips','year'],how='inner')
county_comb_df = county_comb_df[['new_fips','geometry']]
county_comb_df.columns = ['fips','geometry']
county_final_map = county_comb_df.dissolve(by='fips')
county_shapfile_path = os.path.join(cd,r'fips','fips.shp')
county_final_map.to_file(county_shapfile_path,driver='ESRI Shapefile')

# MAKE CFS SHAPEFILE
cfs_crosswalk_path = os.path.join(cd,r'cfs-area-lookup-2007-and-2012.xlsx')
cfs_crosswalk_xls = pd.ExcelFile(cfs_crosswalk_path,engine='openpyxl')
cfs_crosswalk_xls_sheet_names = cfs_crosswalk_xls.sheet_names
cfs_crosswalk = cfs_crosswalk_xls.parse(cfs_crosswalk_xls_sheet_names[1])
cfs_crosswalk = cfs_crosswalk[['ANSI ST','ANSI CNTY','CFS07_AREA','CFS07_NAME']]
##make fips codes
cfs_crosswalk['ANSI ST'] = cfs_crosswalk['ANSI ST'].apply(str)
cfs_crosswalk['ANSI ST'] = cfs_crosswalk['ANSI ST'].str.zfill(2)
cfs_crosswalk['ANSI CNTY'] = cfs_crosswalk['ANSI CNTY'].apply(str)
cfs_crosswalk['ANSI CNTY'] = cfs_crosswalk['ANSI CNTY'].str.zfill(3)
cfs_crosswalk['fips'] = cfs_crosswalk['ANSI ST'] + cfs_crosswalk['ANSI CNTY']
cfs_crosswalk['CFS07_AREA'] = cfs_crosswalk['CFS07_AREA'].apply(str)
cfs_crosswalk['CFS07_AREA'] = cfs_crosswalk['ANSI ST'] + cfs_crosswalk['CFS07_AREA'] 
cfs_crosswalk = cfs_crosswalk[~(cfs_crosswalk['ANSI ST'] == '02') & ~(cfs_crosswalk['ANSI ST'] == '15')]
cfs_crosswalk = cfs_crosswalk[['fips','CFS07_AREA','CFS07_NAME']]
cfs_crosswalk.columns = ['fips', 'cfs_area','cfs_name']
cfs_crosswalk_path = os.path.join(cd,r'cfs07',r'cfs_crosswalk.csv')
cfs_crosswalk.to_csv(cfs_crosswalk_path,index=False)
##join county map and cfs crosswalk
cfs_comb_df = pd.merge(county_final_map,cfs_crosswalk,on='fips',how='inner')
cfs_map = cfs_comb_df.dissolve(by='cfs_name')
cfs_map.reset_index(inplace=True)
cfs_map = cfs_map[['cfs_area','cfs_name','geometry']]
cfs_shapfile_path = os.path.join(cd,r'cfs07','cfs07.shp')
cfs_map.to_file(cfs_shapfile_path,driver='ESRI Shapefile')

# MAKE CZ SHAPEFILE
cz_crosswalk_path = os.path.join(cd,r'cz00_eqv_v1.xls')
cz_crosswalk_xls = pd.ExcelFile(cz_crosswalk_path,engine='xlrd')
cz_crosswalk_xls_sheet_names = cz_crosswalk_xls.sheet_names
cz_crosswalk = cz_crosswalk_xls.parse(cz_crosswalk_xls_sheet_names[0])
cz_crosswalk = cz_crosswalk[['FIPS','Commuting Zone ID, 2000']]
cz_crosswalk['FIPS'] = cz_crosswalk['FIPS'].apply(str)
cz_crosswalk['FIPS'] = cz_crosswalk['FIPS'].str.zfill(5)
cz_crosswalk['Commuting Zone ID, 2000'] = cz_crosswalk['Commuting Zone ID, 2000'].apply(str)
cz_crosswalk['Commuting Zone ID, 2000'] = cz_crosswalk['Commuting Zone ID, 2000'].str.zfill(3)
cz_crosswalk.columns = ['fips', 'cz_area']
cz_crosswalk_path = os.path.join(cd,r'cz00',r'cz_crosswalk.csv')
cz_crosswalk.to_csv(cz_crosswalk_path,index=False)
##join county map and cfs crosswalk
cz_comb_df = pd.merge(county_final_map,cz_crosswalk,on='fips',how='inner')
cz_map = cz_comb_df.dissolve(by='cz_area')
cz_map.reset_index(inplace=True)
cz_map = cz_map[['cz_area','geometry']]
cz_shapfile_path = os.path.join(cd,r'cz00','cz00.shp')
cz_map.to_file(cz_shapfile_path,driver='ESRI Shapefile')

# TEST NEW SHAPEFILES BY PLOTTING
## fips shapefile
county_reload_map = gpd.read_file(county_shapfile_path)
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
county_reload_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.title('FIPS (Consistent) Boundaries')
cfs_plot_path = os.path.join(cd,r'fips','fips_bound_plot.png')
plt.savefig(cfs_plot_path,bbox_inches='tight',dpi=300)

##cfs shapefile
cfs_reload_map = gpd.read_file(cfs_shapfile_path)
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cfs_reload_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.title('CFS (2007) Boundaries')
cfs_plot_path = os.path.join(cd,r'cfs07','cfs_bound_plot.png')
plt.savefig(cfs_plot_path,bbox_inches='tight',dpi=300)

##cz shapfile
cz_reload_map = gpd.read_file(cz_shapfile_path)
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cz_reload_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='gray')
plt.title('CZ (2007) Boundaries')
cz_plot_path = os.path.join(cd,r'cz00','cz_bound_plot.png')
plt.savefig(cz_plot_path,bbox_inches='tight',dpi=300)

