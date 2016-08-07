import csv
import numpy as np

from constants import *

def build_dict_provinces_latlon():
    with open(latlon_csv, "rb") as f:
        rows = csv.reader(f, delimiter=',')

    provinces_latlon = {}
    for row in rows:
        provinces_latlon[row[0]] = (row[1], row[2])

    return provinces_latlon
    
def preprocess_for_rnn(csv_file, pronvices_latlon, num_timesteps=4, stride=1):
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
    
    lats, lons = [], []
    for row in rows:
        lat, lon = province_latlon[row[1]]
        lats.append(lat)
        lons.append(lon)
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)

    mean_lat = np.mean(lats)
    mean_lon = np.mean(lons)
   
    lat_factor = 2/(max_lat - min_lat)
    lon_factor = 2/(max_lon - min_lon)
    data_for_model = []
    for row in rows:
        if row[2] != 'confirmed cases': continue
        num_cases = row[3] 
        lat, lon = province_latlon[row[1]]
        rel_lat = lat_factor * (lat - mean_lat)
        rel_lon = lon_factor * (lon - mean_lon)
        print "lat: %f, lon: %f" % (rel_lat, rel_lon)
        data_for_model.append(np.array([num_cases, rel_lat, rel_lon]))

    return np.array(data_for_model)

if __name__ == "__main__":
    provinces_latlon = build_dict_provinces_latlon(LAT_LON_PROVINCES)
    preprocess_for_rnn(GUINEA_DATA_PATH, provinces_latlon)

