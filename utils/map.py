import pandas as pd
import networkx as nx
import osmnx as ox
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
import geopandas as gpd
import json

ox.config(use_cache=True, log_console=True)


###############
def distance(p1, p2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = p1
    lon2, lat2 = p2
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def nn(ls, point,gdf_nodes):
    nbrs = NearestNeighbors(n_neighbors=1, metric=distance)
    nbrs.fit(ls)
    re = nbrs.kneighbors(point)

    ix = gdf_nodes.iloc[re[1][0][0]].name
    return ix


##########################


def getlocation(address):
    url =  "http://api.positionstack.com/v1/forward?access_key=4b526b911e56291c418c8e4f01dff505&query=" + address+"&region=Los Angeles"

    res = requests.get(url).text
    res = json.loads(res)
    loc = (res["data"][0]["latitude"],res["data"][0]["longitude"])
    return loc


def drawmap(origin,destination,weight1,weight2,weight3):
    gdf_nodes = gpd.read_file(r"utils\nodesandedges\nodes.shp").set_index('osmid')
    gdf_edges = gpd.read_file(r"utils\nodesandedges\final_safety.shp").set_index(['u', 'v', 'key'])
    score = gdf_edges['score'].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    score_scaled = min_max_scaler.fit_transform(score.reshape(-1, 1))
    gdf_edges['score_scaled'] = score_scaled
    gdf_edges['new'] = gdf_edges['length'] *(1+weight1)+ 200/gdf_edges['score_scaled'] * weight3*0.3+gdf_edges['Normalizat']*weight2
    #####################
    u = gdf_edges.index.get_level_values(0).astype("int64")
    v = gdf_edges.index.get_level_values(1).astype("int64")
    key = gdf_edges.index.get_level_values(2).astype("int64")  ####啊啊啊啊！！！！！int64
    gdf_edges = gdf_edges.set_index([u, v, key])
    assert gdf_nodes.index.is_unique and gdf_edges.index.is_unique

    # convert the node/edge GeoDataFrames to a MultiDiGraph
    graph_attrs = {'crs': 'epsg:4326'}
    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs)
    G = ox.utils_graph.get_undirected(G)
    ls = gdf_nodes[['y', "x"]].values

    ##################

    origin = getlocation(origin)
    destination = getlocation(destination)
    origin = [list(origin)]
    destination = [list(destination)]
    orig = nn(ls, origin,gdf_nodes)
    dest = nn(ls, destination,gdf_nodes)
    route = nx.shortest_path(G, orig, dest, weight='new')
    lat = []
    lon = []
    osmid = []
    for i, val in enumerate(route):
        osmid.append(val)
        lat.append(G.nodes[val]['y'])
        lon.append(G.nodes[val]['x'])
    routept = pd.DataFrame({"osmid": osmid, "lat": lat, "lon": lon})
    fig = go.Figure(go.Scattermapbox(
        mode="lines",
        lon=routept['lon'],
        lat=routept['lat'],
        marker={'size': 10,'color': 'Blue'}))
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[routept.iloc[0,2],routept.iloc[-1,2]],
        lat=[routept.iloc[0,1],routept.iloc[-1,1]],
        marker={'size': 10,'color': 'Blue'}))
    fig.update_traces(line=dict(color="Blue", width=4))           #for change the style of line
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=13, mapbox_center_lat = 34.0347,mapbox_center_lon = -118.2712,
        margin={"r":0,"t":0,"l":0,"b":0},height=800,showlegend = False)

    #fig.show()

    return fig