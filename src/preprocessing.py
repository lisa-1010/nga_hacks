# preprocessing.py
# @author: Lisa Wang, Nish Khandwala
# @created: August 6, 2016
#
#===============================================================================
# DESCRIPTION:
#
# To preprocess the csv data files to numpy matrices, split into train and test
# which are ready to be fed into an RNN.
#
#===============================================================================
# CURRENT STATUS: Working
#===============================================================================
# USAGE: python preprocessing.py
#===============================================================================

import csv
import numpy as np

from sklearn.cross_validation import train_test_split

from constants import *
from collections import defaultdict

def build_dict_provinces_latlon(latlon_csv):
    provinces_latlon = {}
    with open(latlon_csv, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            provinces_latlon[row[0]] = (float(row[1]), float(row[2]))
    return provinces_latlon

def compute_mean_and_scaling_factor(lats, lons):
    min_lat, max_lat = np.min(lats), np.max(lats)
    min_lon, max_lon = np.min(lons), np.max(lons)

    mean_lat = np.mean(lats)
    mean_lon = np.mean(lons)

    scale_lat = 2.0 / (max_lat - min_lat)
    scale_lon = 2.0 / (max_lon - min_lon)
    return mean_lat, mean_lon, scale_lat, scale_lon


def preprocess_for_rnn(csv_file, provinces_latlon, num_timesteps=4, stride=1):
    f = open(csv_file, "rb")
    rows = csv.reader(f, delimiter=',')
    
    lats, lons = [], []
    raw_data_dict = defaultdict(list)
    for row in rows:
        if row[2] != 'confirmed cases': continue
        lat, lon = provinces_latlon[row[1]]
        lats.append(float(lat))
        lons.append(float(lon))
        raw_data_dict[row[1]].append(row[3:])
    f.close()


    mean_lat, mean_lon, scale_lat, scale_lon = compute_mean_and_scaling_factor(lats, lons)

    print ("mean lat: {} \t mean lon: {} \t scale lat: {} \t scale lon: {}".format(mean_lat, mean_lon, scale_lat, scale_lon ))

    data = []
    labels = []

    print "number of provinces {}".format(len(raw_data_dict))

    for province, rows in raw_data_dict.iteritems():
        # for each province, go through all the rows:
        lat, lon = provinces_latlon[province]
        rel_lat = scale_lat * (lat - mean_lat)
        rel_lon = scale_lon * (lon - mean_lon)
        print ("rel_lat: {} \t rel_lon: {}".format(rel_lat, rel_lon))

        for i in xrange(len(rows) - num_timesteps - 1):
            # since we are predicting the next timestep, we don't use the features from the last
            # timestep, since we wouldn't know what the prediction would be.

            sample_across_timesteps = np.array([[rows[i+j][0], rel_lat, rel_lon] for j in xrange(num_timesteps)])
            data.append(sample_across_timesteps)

            # for j in xrange(num_timesteps):
            #     data.append(np.array([rows[i+j][0], rel_lat, rel_lon]))
            labels.append(rows[i+j+1][0])


    dataset = train_test_split(np.array(data), np.array(labels), test_size = 0.10, random_state = 42)
    # import pdb; pdb.set_trace()
    np.save(PREPROCESSED_DATA, dataset)


def test_data():
    X_train, X_test, y_train, y_test = np.load(PREPROCESSED_DATA)

    print ("{} {} {} {}".format(X_train.shape, X_test.shape, y_train.shape, y_test.shape))

if __name__ == "__main__":
    provinces_latlon = build_dict_provinces_latlon(LAT_LON_PROVINCES)
    # print provinces_latlon
    preprocess_for_rnn(GUINEA_DATA_PATH, provinces_latlon)
    test_data()

