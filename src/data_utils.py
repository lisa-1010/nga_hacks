import csv
import numpy as np
from collections import Counter
import pprint
import copy
import re

from constants import *

def lower_entire_csv(csv_file):
    lower_rows = []
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            lower_rows.append([w.lower() for w in row])

    with open(csv_file, "wb") as f:
        writer = csv.writer(f,  delimiter=',')
        for row in lower_rows:
            writer.writerow(row)


def filter_by_country(source_file, country_file, country="guinea"):
    with open(source_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        country_specific_rows = [row for row in rows if row[0] == country]
    with open(country_file, "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for row in country_specific_rows:
            writer.writerow(row)


def find_case_types(csv_file):
    case_types = set()
    case_types_count = Counter()
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            case_types.add(row[2])
            case_types_count[row[2]] += 1
    # print case_types
    print case_types_count
    return case_types_count


def count_num_provinces(csv_file):
    num_regions = 0
    # provinces = set()
    provinces = Counter()
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            provinces[row[1]] += 1
    print "number of provinces: {}".format(len(provinces.keys()))
    return provinces


def find_number_of_cases_in_each_case_type():

    with open(CLEAN_DATA_PATH, "rb") as f:
        rows = csv.reader(f, delimiter=',')

        #print len([row for row in rows if (row[0] == "Guinea" and row[2] )


def merge_three_countries():
    all_rows = []
    for country_file in COUNTRIES_DATA_PATHS:
        with open(country_file, "rb") as f:
            rows = csv.reader(f, delimiter=',')
            for row in rows:
                all_rows.append(row)
    with open(ALL_THREE_COUNTRIES_DATA_PATH, "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for row in all_rows:
            writer.writerow(row)


def remove_invalid_provinces(country_file, provinces_file):
    valid_provinces = set()
    with open(provinces_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            valid_provinces.add(row[0])

    print valid_provinces
    new_rows = []

    excluded_provinces = set()
    with open(country_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            row[1] = row[1].strip()
            if row[1] == 'for\xc3\xa9cariah':
                row[1] = 'forecariah'
            elif row[1] == 'lab\xc3\xa9':
                row[1] = 'labe'
            elif row[1] == 'tougu\xc3\xa9':
                row[1] = 'tougue'
            elif row[1] == 'port':
                row[1] = 'port loko'

            if row[1] in valid_provinces:
                new_rows.append(row[:-2])

            else:
                excluded_provinces.add(row[1])
                # print 'exluding province {}'.format(row[1])

    # print len(new_rows)
    print "excluded provinces: {}".format(excluded_provinces)
    with open(country_file, "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for row in new_rows:
            writer.writerow(row)


if __name__ == "__main__":
    # lower_entire_csv(RAW_DATA_PATH)
    # find_case_types()
    # filter_by_country(CLEAN_DATA_PATH, GUINEA_DATA_PATH, country="guinea")
    # filter_by_country(CLEAN_DATA_PATH, LIBERIA_DATA_PATH, country="liberia")
    # filter_by_country(CLEAN_DATA_PATH, SIERRA_DATA_PATH, country="sierra leone")

    # for country, country_file in zip(COUNTRIES, COUNTRIES_DATA_PATHS):
    #     print country
    #     count_num_provinces(country_file)
    #     find_case_types(country_file)

    # merge_three_countries()
    # lower_entire_csv(LAT_LON_PROVINCES)
    pp = pprint.PrettyPrinter()
    # pp.pprint( count_num_provinces(ALL_THREE_COUNTRIES_DATA_PATH))



    for country, country_file in zip(COUNTRIES, COUNTRIES_DATA_PATHS):
        print country
        remove_invalid_provinces(country_file, LAT_LON_PROVINCES)

    remove_invalid_provinces(ALL_THREE_COUNTRIES_DATA_PATH, LAT_LON_PROVINCES)
