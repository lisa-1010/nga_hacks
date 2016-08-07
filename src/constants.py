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
LAT_LON_PROVINCES = "../data/lat-lon-provinces.csv"

PREPROCESSED_DATA = "../data/preprocessed.npy"

COUNTRIES = ["guinea", "liberia", "sierra leone"]

COUNTRIES_DATA_PATHS = [GUINEA_DATA_PATH, LIBERIA_DATA_PATH, SIERRA_DATA_PATH]
