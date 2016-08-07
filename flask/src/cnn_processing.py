import numpy as np
from preprocessing import *
from sklearn.cross_validation import train_test_split

degree_interval = 0.08
num_timesteps = 10

def fill_grid(grid, clean_dict, cardinals):
    north, south, east, west = cardinals
    grid_province_dict = {}
    for province, rows in clean_dict.iteritems():
        rows = sorted(rows, key=lambda x: (x[4]))  # sort by date
        x = int(np.floor((rows[0][6] - west)/degree_interval))
        y = int(np.floor((rows[0][5] - south)/degree_interval))
        if (x, y) in grid_province_dict: # HACKY AF
            x += 1
            y += 1
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
    if num_x > num_y:
        north += num_x - num_y
        num_y = num_x
    else:
        east += num_y - num_x 
        num_x = num_y

    return num_x, num_y, (north, south, east, west)

def get_grid(clean_dict):
    lats, lons = [], []
    for province, rows in clean_dict.iteritems():
        lats.append(rows[0][5])
        lons.append(rows[0][6])
    num_x, num_y, cardinals = calculate_grid_size(lats, lons)
    num_grids = len(clean_dict[clean_dict.keys()[0]])
    grid = np.zeros((num_grids, num_x, num_y, 1))
    return fill_grid(grid, clean_dict, cardinals)

def get_data(clean_dict):
    grid, grid_province_dict = get_grid(clean_dict)
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

    return X, y, mask, grid_province_dict

def get_train_test(X, y, test_percent=0.10):
    return train_test_split(X, y, test_size=test_percent, random_state=42)
 
def preprocess_for_cnn(clean_csv_file=CLEAN_GUINEA_DATA_PATH, dataset_name="guinea",
                                         num_timesteps=25, case_type="confirmed cases"):
    clean_dict = load_clean_data_dict_aligned_by_time(clean_csv_file, dataset_name, num_timesteps, case_type)
    X, y, mask, grid_province_dict = get_data(clean_dict)
    X_train, X_test, y_train, y_test = get_train_test(X, y)
    np.save('cnn_data', (X_train, X_test, y_train, y_test, mask, grid_province_dict))

if __name__ == '__main__':
    preprocess_for_cnn()
