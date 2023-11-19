#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import geopandas as gpd
import os, shutil
import rasterio
import urllib
import re
import fiona
from shapely.geometry import box
import fiona.transform
import requests
import json
from rasterstats import zonal_stats


# ### Use Cloud Optimized Geotiffs for faster analysis of NAIP imagery
# #### Using the code below, NAIP imagery will be streamed rather than downloaded for faster calculation of the NDVI for 
# #### each NAIP quad, which will then be reclassified (vegetation/no vegetation) to be a rough indicator of the presence of fuel.
# 
# #### For each structure (from Microsoft footprint structures) in the CalFire damage inventory dataset, a perimeter of 30 and 100 feet
# #### are used to assess the vegetation around the home using the reclassified NDVI, to determine whether the clearance
# #### of vegetation surrounding the structure has an impact on the structure's survival.

# In[ ]:


basepath = r'D:\SIE512\finalproject'


# In[ ]:


# Take the centroids of the processed structure data
aoi = gpd.read_file(os.path.join(basepath,'centroid.gpkg'))


# In[ ]:


# add an index column to refer back to later
aoi['indexnum'] = aoi.index


# In[ ]:


ntiles = gpd.GeoDataFrame.from_file(os.path.join(basepath,'NAIP_18_CA.shp')) #quad coverage file from Azure


# In[ ]:


# Change the projection to match the NAIP quads
print(aoi.crs, ntiles.crs)
ntiles=ntiles.to_crs('epsg:26910')
print(aoi.crs, ntiles.crs)


# In[ ]:


# Join the structure centroids to the quad metadata to get the file name for each point
quad_intersection = gpd.sjoin(ntiles, aoi, how="right", op='intersects')


# In[ ]:


# sort so that the NAIP images with the most points get processed first
quad_intersection['counts'] = quad_intersection.groupby(['FileName'])['FileName'].transform('count')
quad_intersection = quad_intersection.sort_values(by='counts',ascending=False)
quadlist = quad_intersection.FileName.unique()


# In[ ]:


# Reassign the index of the file - for later joining. Rasterstats does not preserve id fields and creates it's own index
quad_intersection['id'] = quad_intersection.index


# In[ ]:


# get rid of unneeded columns
ql = quad_intersection[['geometry','FileName','id']]
ql = ql.to_crs(epsg=26910)


# In[ ]:


#load the buffered structure points
qin30 = gpd.GeoDataFrame.from_file(os.path.join(basepath,'buff3026910.gpkg'))
qin100 = gpd.GeoDataFrame.from_file(os.path.join(basepath,'buff10026910.gpkg'))

# create new index field for matching
qin30['id'] = qin30.index
qin100['id'] = qin100.index

# reproject to the NAIP file projection
qin30=qin30.to_crs(epsg=26910)
qin100=qin100.to_crs(epsg=26910)

# Join the quad file names with the buffer
quad30 = ql.merge(qin30, on='id')
quad100 = ql.merge(qin100, on='id')


# In[ ]:


# Remove uncessary fields to use less memory
quad30 = quad30[['FileName', 'id', 'geometry_y']]
quad100 = quad100[['FileName', 'id', 'geometry_y']]


# In[ ]:


# How many NAIP tiles there are to load
print(len(quadlist))


# In[ ]:


import numpy as np

# The parameters for the NAIP imagery
year = '2018'
state = 'ca'
resolution = '060cm'

# Azure blob location
blob_root = 'https://naipeuwest.blob.core.windows.net/naip'


y=0
for filen in quadlist:
    print(y)
    y=y+1
    
    # Get the name of the file and create the link to the tile
    quadrangle = filen[2:7]
    filename = filen
    tile_url = blob_root + '/v002/' + state + '/' + year + '/' + state + '_' + resolution +     '_' + year + '/' + quadrangle + '/' + filename
    print(tile_url)
    
    if not os.path.exists(os.path.join(basepath,'results',filen + '_100*.csv')):
        #Get the subset of def space perimeters to process based on the tif filename
        q30, q100 = quad30.loc[quad30.FileName == filen],quad100.loc[quad100.FileName == filen]
        qlist = [q30,q100]
        
        with rasterio.open(tile_url) as f:
            # read the red and nir bands to calculate NDVI
            red,nir = f.read(1).astype('float64'),f.read(4).astype('float64')

            # set transform for zonal_stats
            affine= f.transform

            # Calculate NDVI and reclassify to fuel/no fuel
            # Threshold of .1 for vegetation
            print('Calculate NDVI')
            ndvi = np.where((nir+red) == 0, 0, (nir-red)/(nir+red))
            ndvi[ndvi>.1] = 1
            ndvi[ndvi<=.1] = 0

            print('Open polygons')
            n=0
            
            # Output csv files for each NAIP tile - concatenate them later rather than risk losing data
            # to error, internet connectivity issues, etc
            for q in qlist:
                if n==0:
                    fn = 'p30'
                    x = pd.DataFrame(pd.Series(q.id))
                    x.to_csv(filen + '_30.csv')
                else:
                    fn = 'p100'
                    x = pd.DataFrame(pd.Series(q.id))
                    x.to_csv(filen + '_100.csv')
                print(fn)
                
                outdf = pd.DataFrame()
                
                # For each polygon, use zonal_stats to calculate the # of pixels (veg/no veg)
                for i, row in q.iterrows():
                    p = row[-1]
                    a = zonal_stats(p, ndvi, affine=affine, categorical=True,keep_ids=True)
                    print(a)
                    
                    # Create a list of the index and the stats and output to csv
                    abc = [(a,i)]
                    fn_out = fn + filename[:-4] +'.csv'
                    outdf=outdf.append(abc)
                    
                outdf.to_csv(fn_out)
                n=n+1


# In[ ]:


x = 'test_ndvi.tif'
with rasterio.open(x, 'w', 
                           driver='GTiff',
                           height=f.shape[0],
                           width=f.shape[1],
                           count=1,
                           dtype='float64', #'float64',# 'uint8' for scaled ndvi
                           crs=f.crs,
                           transform=affine) as dst:
                               dst.write(ndvi,1)


# In[ ]:


def bulkDF(inpath, parameter, outfile):
    all_files30 = glob.glob(path + parameter)
    
    llist = []
    
    for filename in allfiles:
        df = pd.read_csv(filename, index_col=None, header=0)
        llist.append(df)
    dfout = pd.concat(llist, axis=0, ignore_index=True)
    print(dfout.head())
    return dfout

bulkdf(os.path.join(basepath, results),"\p30*.csv",os.path.join(basepath, results,"30results.csv"))
bulkdf(os.path.join(basepath, results),"\p100*.csv",os.path.join(basepath, results,"100results.csv"))
bulkdf(os.path.join(basepath, results),"\*.tif_30.csv",os.path.join(basepath, results,"30index.csv"))
bulkdf(os.path.join(basepath, results),"\*.tif_100.csv",os.path.join(basepath, results,"100index.csv"))


# In[ ]:




