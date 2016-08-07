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
import sys

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


def clean_data_convert_dates_make_normalize_lat_lon(csv_file, dataset_name):
    # Cleans the csv file by converting the date into days from the first day.
    # Also looks up lat lon for the province and normalizes them.
    # Saves clean data to a new csv.
    provinces_latlon = build_dict_provinces_latlon(LAT_LON_PROVINCES)
    first_date = find_first_date(csv_file)
    f = open(csv_file, "rb")
    rows = csv.reader(f, delimiter=',')

    lats, lons = [], []
    raw_data_dict = defaultdict(list)
    for row in rows:
        try:
            # since sometimes the data entry is ill-formatted
            row[3] = int(row[3])
        except:
            continue

        total_days_since_day_zero = int((parse(row[4]) - first_date).total_seconds() / (60 * 60 * 24))
        row[4] = total_days_since_day_zero
        lat, lon = provinces_latlon[row[1]]  # get lat lon for this province from dict
        lats.append(float(lat))
        lons.append(float(lon))
        raw_data_dict[row[1]].append(row)
    f.close()

    mean_lat, mean_lon, scale_lat, scale_lon = compute_mean_and_scaling_factor(lats, lons)

    clean_rows = []
    for province, rows in raw_data_dict.iteritems():
        # for each province, go through all the rows:
        rows = sorted(rows, key=lambda x: (x[-1]))  # sort by date

        lat, lon = provinces_latlon[province]
        rel_lat = float(scale_lat * (lat - mean_lat))
        rel_lon = float(scale_lon * (lon - mean_lon))

        for row in rows:
            row.extend([rel_lat, rel_lon])

        clean_rows.extend(rows)

    with open("../data/" + dataset_name + "_clean.csv", "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for row in clean_rows:
            writer.writerow(row)

def get_data_dict_from_clean_csv(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea", case_type="confirmed_cases"):
    data_dict_by_province = defaultdict(list)
    with open(clean_csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            if row[2] == case_type:
                data_dict_by_province[row[1]].append(row)
    return data_dict_by_province


def convert_clean_csv_to_numpy_for_rnn(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea",  num_timesteps=25, case_type = "confirmed cases"):
    data_dict_by_province = get_data_dict_from_clean_csv(clean_csv_file=clean_csv_file, dataset_name=dataset_name, case_type=case_type)
    data = []
    labels = []

    for province, rows in data_dict_by_province.iteritems():
        print "processing for province: {}".format(province)
        # for each province, go through all the rows:
        rows = sorted(rows, key=lambda x: (x[4]))  # sort by date

        for i in xrange(len(rows) - num_timesteps - 1):
            # since we are predicting the next timestep, we don't use the features from the last
            # timestep, since we wouldn't know what the prediction would be.
            sample_across_timesteps = []
            # prev_num_cases = 0
            for j in xrange(num_timesteps):
                num_cases, rel_lat, rel_lon = int(rows[i + j][3]), float(rows[i + j][5]), float(rows[i + j][6])
                # if num_cases < prev_num_cases:
                #     # to account for odd numbers in the data, where the number of cases decreases
                #     num_cases = prev_num_cases
                # prev_num_cases = num_cases
                sample_across_timesteps.append(np.array([num_cases, rel_lat, rel_lon]))
            data.append(np.array(sample_across_timesteps))
            labels.append(int(rows[i + num_timesteps][3]))

    dataset = train_test_split(np.array(data), np.array(labels), test_size=0.10, random_state=42)

    np.save("../data/preprocessed/" + dataset_name + "_" + str(num_timesteps) + ".npy", dataset)
    print ("finished processing data to numpy.")


def find_first_and_last_entry(rows):
    rows = sorted(rows, key=lambda x: (x[4])) # sort by date
    return int(rows[0][4]), int(rows[-1][4])



def find_first_and_last_shared_days(data_dict_by_province):

    first_shared_day = -sys.maxint - 1
    last_shared_day = sys.maxint
    for province, rows in data_dict_by_province.iteritems():
        first_day, last_day = find_first_and_last_entry(rows)
        print "Province: {} \t first day: {} \t last day: {}".format(province, first_day, last_day)
        first_shared_day = max(first_shared_day, first_day)
        last_shared_day = min(last_shared_day, last_day)
    return first_shared_day, last_shared_day


def create_data_for_extrapolation_aligned_by_time(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea", num_timesteps=25, case_type="confirmed cases"):
    data_dict_by_province = get_data_dict_from_clean_csv(clean_csv_file=clean_csv_file, dataset_name=dataset_name,
                                                         case_type=case_type)


    provinces, data, labels =[], [], []

    new_data_dict_by_province = defaultdict(list)
    for province, rows in data_dict_by_province.iteritems():
        rows = sorted(rows, key=lambda x: (x[4]))  # sort by date
        first_day, last_day = find_first_and_last_entry(rows)
        if first_day > 250:
            print "first day too late. Skipping province {}".format(province)
            continue
        new_data_dict_by_province[province] = rows

    first_shared_day, last_shared_day = find_first_and_last_shared_days(new_data_dict_by_province)




    for province, rows in new_data_dict_by_province.iteritems():
        rows = sorted(rows, key=lambda x: int(x[4]))  # sort by date
        # print rows
        # selected_rows.append(filter(lambda x: int(x[4]) == first_shared_day, rows)[0])
        # selected_rows.append(rows.find(lambda x: int(x[4]) == first_shared_day))

        i = (m for m, r in enumerate(rows) if int(r[4]) >= 250).next()

        print rows[i]
        # since we are predicting the next timestep, we don't use the features from the last
        # timestep, since we wouldn't know what the prediction would be.
        sample_across_timesteps = []
        # prev_num_cases = 0
        for j in xrange(num_timesteps):
            num_cases, rel_lat, rel_lon = int(rows[i + j][3]), float(rows[i + j][5]), float(rows[i + j][6])
            # if num_cases < prev_num_cases:
            #     # to account for odd numbers in the data, where the number of cases decreases
            #     num_cases = prev_num_cases
            # prev_num_cases = num_cases
            sample_across_timesteps.append(np.array([num_cases, rel_lat, rel_lon]))

        provinces.append(province)
        data.append(np.array(sample_across_timesteps))
        labels.append(int(rows[i + num_timesteps][3]))

    dataset = data, provinces

    np.save("../data/preprocessed/" + dataset_name + "_" + str(num_timesteps) + "_for_extrapolation.npy", dataset)
    print ("finished processing data for extrapolation.")

    # data, provinces = np.load("../data/preprocessed/" + dataset_name + "_" + str(num_timesteps) + "_for_extrapolation.npy")
    #
    # print data[0]
    # print provinces[0]


if __name__ == "__main__":
    # for country, country_file in zip(COUNTRIES, COUNTRIES_DATA_PATHS):
    #     clean_data_convert_dates_make_normalize_lat_lon(country_file, country)

    # for clean_country_file, country in zip(COUNTRIES_CLEAN_DATA_PATHS, COUNTRIES):
    #     convert_clean_csv_to_numpy_for_rnn(clean_country_file, dataset_name=country)
    #

    create_data_for_extrapolation_aligned_by_time()
