import csv
from collections import Counter

RAW_DATA_PATH = "data/data-ebola-public.csv"
CLEAN_DATA_PATH = "data/data-ebola-public-clean.csv"
GUINEA_DATA_PATH = "data/guinea.csv"
LIBERIA_DATA_PATH = "data/liberia.csv"
SIERRA_DATA_PATH = "data/sierra.csv"

countries = ["guinea", "liberia", "sierra leone"]


def lower_entire_csv(csv_file):
    lower_rows = []
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            lower_rows.append([w.lower() for w in row])

    with open(CLEAN_DATA_PATH, "wb") as f:
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
    provinces = set()
    with open(csv_file, "rb") as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            provinces.add(row[1])
    print "number of provinces: {}".format(len(provinces))


def find_number_of_cases_in_each_case_type():

    with open(CLEAN_DATA_PATH, "rb") as f:
        rows = csv.reader(f, delimiter=',')

        #print len([row for row in rows if (row[0] == "Guinea" and row[2] )


if __name__ == "__main__":
    # lower_entire_csv(RAW_DATA_PATH)
    # find_case_types()
    # filter_by_country(CLEAN_DATA_PATH, GUINEA_DATA_PATH, country="guinea")
    # filter_by_country(CLEAN_DATA_PATH, LIBERIA_DATA_PATH, country="liberia")
    # filter_by_country(CLEAN_DATA_PATH, SIERRA_DATA_PATH, country="sierra leone")

    for country, country_file in zip(countries, [GUINEA_DATA_PATH, LIBERIA_DATA_PATH, SIERRA_DATA_PATH]):
        print country
        count_num_provinces(country_file)
        find_case_types(country_file)