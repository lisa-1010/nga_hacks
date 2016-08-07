import numpy as np
from preprocessing import *

degree_interval = 0.5

def fill_grid(grid, clean_dict, cardinals):
    north, south, east, west = cardinals
	grid_province_dict = {}
    for province, rows in clean_dict.iteritems():
        rows = sorted(rows, key=lambda x: (x[4]))  # sort by date
        x = int(np.floor((rows[0][6] - west)/degree_interval))
        y = int(np.floor((rows[0][5] - south)/degree_interval))
		grid_province_dict[(x, y)] = province
        for t in range(len(rows)):
            feat = rows[t][4]
            grid[t, x, y, 0] += feat
    return grid, grid_province_dict

def calculate_grid_size(latitudes, longitudes):
    north = np.ceil(max(latitudes) * 2.0) / 2.0
    south = np.floor(min(latitudes) * 2.0) / 2.0
    east = np.ceil(max(longitudes) * 2.0) / 2.0
    west = np.floor(min(longitudes) * 2.0) / 2.0

    num_y = int((north - south) / degree_interval)
    num_x = int((east - west) / degree_interval)
    return num_x, num_y, (north, south, east, west)

def get_grid(clean_dict):
    lats, lons = []
    for province, rows in clean_dict.iteritems():
        lats.append(rows[0][5])
        lons.append(rows[0][6])
    num_x, num_y, cardinals = calculate_grid_size(lats, lons)
    num_grids = len(clean_dict[clean_dict.keys()[0]]
    grid = np.zeros((num_grids, num_x, num_y, 1))
    return fill_grid(grid, clean_dict, cardinals)

def get_data(clean_dict):
    grid = get_grid(clean_dict)
    X, y = [], []
    timescale, num_rows, num_cols, num_features = grid.shape
    for t in range(num_timesteps, timescale):
        X.append(grid[t - num_timesteps: t])
        y_t = np.zeros((num_rows, num_cols))
        for i in range(num_rows):
            for j in range(num_cols):
                y_t[i, j] = grid[t, i, j, 0]
        y.append(y_t)
    X = np.array(X)
    y = np.array(y)

    mask = np.ones((num_rows, num_cols))
    for i in range(num_rows):
        for j in range(num_cols):
            if np.sum(grid[:, i, j, 0]) == 0:
                mask[i, j] = 0

    return X, y, mask 
   
def preprocess_for_cnn(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea", num_timesteps=25, case_type="confirmed cases"):
    data_dict_by_province = get_data_dict_from_clean_csv(clean_csv_file=clean_csv_file, dataset_name=dataset_name, case_type=case_type)

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
        # row = ["guinea", "province", "cases", 4, 199, lat, lon]    
        rows = sorted(rows, key=lambda x: int(x[4]))  # sort by date

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

def convert_clean_csv_to_numpy_for_rnn(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea",  num_timesteps=25, case_type = "confirmed cases"):
    data_dict_by_province = get_data_dict_from_clean_csv(clean_csv_file=clean_csv_file, dataset_name=dataset_name, case_type=case_type)
    data = []
    labels = []

    first_shared_day, last_shared_day = find_first_and_last_shared_days(data_dict_by_province)
    


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
'''

if __name__ == '__main__':
    preprocess_for_cnn()
