# constants.py
# @author: Lisa Wang
# @created: August 6, 2016
#
#===============================================================================
# DESCRIPTION:
#
# A place to put constants used across this repo.
#
#===============================================================================
# CURRENT STATUS: Working
#===============================================================================
# USAGE: from constants import *
#===============================================================================

RAW_DATA_PATH = "../data/data-ebola-public.csv"
CLEAN_DATA_PATH = "../data/data-ebola-public-clean.csv"

GUINEA_DATA_PATH = "../data/guinea.csv"
LIBERIA_DATA_PATH = "../data/liberia.csv"
SIERRA_DATA_PATH = "../data/sierra.csv"
ALL_THREE_COUNTRIES_DATA_PATH = "../data/all_three_countries.csv"

CLEAN_GUINEA_DATA_PATH = "../data/guinea_clean.csv"
CLEAN_LIBERIA_DATA_PATH = "../data/liberia_clean.csv"
CLEAN_SIERRA_DATA_PATH = "../data/sierra_clean.csv"
CLEAN_ALL_THREE_COUNTRIES_DATA_PATH = "../data/all_three_countries_clean.csv"

LAT_LON_PROVINCES = "../data/lat-lon-provinces.csv"

PREPROCESSED_GUINEA_DATA = "/Users/lisa1010/dev/nga_hacks/flask/data/preprocessed/guinea_25.npy"
PREPROCESSED_DATA = "../data/preprocessed.npy"

PREPROCESSED_GUINEA_DATA_EXTRA = "/Users/lisa1010/dev/nga_hacks/flask/data/preprocessed/guinea_25_for_extrapolation.npy"

COUNTRIES = ["guinea", "liberia", "sierra", "all_three_countries"]

COUNTRIES_DATA_PATHS = [GUINEA_DATA_PATH, LIBERIA_DATA_PATH, SIERRA_DATA_PATH, ALL_THREE_COUNTRIES_DATA_PATH]
COUNTRIES_CLEAN_DATA_PATHS = [CLEAN_GUINEA_DATA_PATH, CLEAN_LIBERIA_DATA_PATH, CLEAN_SIERRA_DATA_PATH, CLEAN_ALL_THREE_COUNTRIES_DATA_PATH]

