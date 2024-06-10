import pandas as pd
import networkx as nx
import osmnx as ox
import requests
import numpy as np
import os
import sys

# This file contains all the cities, even smaller ones. Better to clean it first with a subset of the cities we are interested. 
fileCHS = 'GHS_STAT_UCDB2015MT_GLOBE_R2019A_V1_2.csv' 
df =  pd.read_csv(fileCHS)

#paths to handle the different types of data. Modify accordlingly
outfile = 'errors.csv'
input_path = ''
output_path = ""

f = open(outfile,"w+")

for row in df.itertuples():
    strc=row.ID_HDC_G0
    strc = row.UC_NM_MN[:-6]+","+row.CTR_MN_NM
    print(strc)
    #Get the bounding box for each city
    north, south, east, west = row.BBX_LATMX,row.BBX_LATMN,row.BBX_LONMX,row.BBX_LONMN
    #Download street network from osmnx using 
    try:
	G = ox.graph_from_bbox(north, south, east, west,network_type='drive',simplify=True) # Network type could be altered to get a full network including walking paths.
	#further cleaning
    	multi_di_graph_utm = ox.project_graph(G)
    	multi_di_graph_cons = ox.consolidate_intersections(multi_di_graph_utm, tolerance=10, dead_ends=False)
    except:
        print('Error at ' + str(strc))
        f.write("%s\n" % str(strc))
f.close()
