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
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


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


def find_first_date(csv_file):
    f = open(csv_file, "rb")
    rows = csv.reader(f, delimiter=',')
    dates = set()
    for row in rows:
        dates.add(parse(row[4]))
    dates_list = list(dates)
    dates_list.sort()

    print ("first date: {}".format(dates_list[0]))
    f.close()
    return dates_list[0]

def calculate_date_diff(first_date, last_date):
    # *_date are dateutil module instances
    return (last_date.year - first_date.year)*12*365 + (last_date.month - first_date.month) * 30 + first_date.day

# def summarize_by_week(rows):
#     # takes rows for particular province
#
#     print "summarize 10"
#     print rows[:10]
#     # for row in rows:

def preprocess_for_rnn(csv_file, provinces_latlon, num_timesteps=25, stride=1):

    first_date = find_first_date(csv_file)
    f = open(csv_file, "rb")
    rows = csv.reader(f, delimiter=',')
    
    lats, lons = [], []
    raw_data_dict = defaultdict(list)
    for row in rows:
        if row[2] != 'confirmed cases': continue
        if row[3] == '': continue
        try:
            # since sometimes the data entry is ill-formatted
            row[3] = int(row[3])
        except:
            continue

        total_days_since_day_zero = int((parse(row[4]) - first_date).total_seconds() / (60 * 60 * 24))
        row[4] = total_days_since_day_zero
        lat, lon = provinces_latlon[row[1]] # get lat lon for this province from dict
        lats.append(float(lat))
        lons.append(float(lon))
        raw_data_dict[row[1]].append(row)
    f.close()

    mean_lat, mean_lon, scale_lat, scale_lon = compute_mean_and_scaling_factor(lats, lons)

    convert_raw_data_to_numpy(raw_data_dict, num_timesteps, provinces_latlon, mean_lat, mean_lon, scale_lat, scale_lon)

    # print ("mean lat: {} \t mean lon: {} \t scale lat: {} \t scale lon: {}".format(mean_lat, mean_lon, scale_lat, scale_lon ))



def convert_raw_data_to_numpy(raw_data_dict, num_timesteps, provinces_latlon, mean_lat, mean_lon, scale_lat, scale_lon):
    # takes in a dict mapping each province to all the rows
    data = []
    labels = []

    print "number of provinces {}".format(len(raw_data_dict))

    for province, rows in raw_data_dict.iteritems():
        # for each province, go through all the rows:
        rows = sorted(rows, key=lambda x: (x[-1])) # sort by date

        print province
        # print np.array(rows)[:, -1]

        # summarize_by_week(rows)
        lat, lon = provinces_latlon[province]
        rel_lat = float(scale_lat * (lat - mean_lat))
        rel_lon = float(scale_lon * (lon - mean_lon))
        print ("rel_lat: {} \t rel_lon: {}".format(rel_lat, rel_lon))

        for i in xrange(len(rows) - num_timesteps - 2):
            # since we are predicting the next timestep, we don't use the features from the last
            # timestep, since we wouldn't know what the prediction would be.

            sample_across_timesteps = []
            for j in xrange(num_timesteps):
                # print rows[i+j]
                sample_across_timesteps.append([int(rows[i + j][3]), rel_lat, rel_lon])
                # sample_across_timesteps = np.array([[int(rows[i+j][0]), rel_lat, rel_lon] for j in xrange(num_timesteps)])
            data.append(np.array(sample_across_timesteps))

            # for j in xrange(num_timesteps):
            #     data.append(np.array([rows[i+j][0], rel_lat, rel_lon]))
            labels.append(int(rows[i + num_timesteps][3]))

    dataset = train_test_split(np.array(data), np.array(labels), test_size=0.10, random_state=42)

    np.save(PREPROCESSED_DATA, dataset)
    print ("finished processing data to numpy.")



def test_data():
    X_train, X_test, y_train, y_test = np.load(PREPROCESSED_DATA)

    print ("{} {} {} {}".format(X_train.shape, X_test.shape, y_train.shape, y_test.shape))
    print X_train[0]
    print y_train[0]
    print y_train[0].dtype




if __name__ == "__main__":
    # provinces_latlon = build_dict_provinces_latlon(LAT_LON_PROVINCES)
    # preprocess_for_rnn(GUINEA_DATA_PATH, provinces_latlon)

    test_data()

    # find_first_date(GUINEA_DATA_PATH)

