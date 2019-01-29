#!/usr/bin/env python
# -*- coding: utf-8 -*-

from global_parameters import *
import pandas as pd
import pickle

def cal_vehicles():
    data = pd.DataFrame(columns=('vehicle_ID',
                                 'start_loc',
                                 'start_time',
                                 'stop_time',
                                 )
                      )
    for i in range(VEHICLES_NUMS):
        start_loc = np.random.randint(1, GRID_NUMS)
        start_time = int(np.random.triangular(0, 8 * 60, 24 * 60))
        temp = start_time + np.random.randint(8 * 60, 12 * 60)
        stop_time = temp if temp < 1440 else temp - 1440
        data.loc[i] = [i, start_loc, start_time, stop_time]
    vehicle_dict = {}
    for key in range(1440):
        vehicle_dict[key] = []
        for i in range(VEHICLES_NUMS):
            if (data.loc[i, 'stop_time'] < data.loc[i, 'start_time'] and data.loc[i, 'stop_time'] >= key) \
                or (data.loc[i, 'stop_time'] > data.loc[i, 'start_time'] and (key <= data.loc[i, 'stop_time'] and key >= data.loc[i, 'start_time'])):
                vehicle_dict[key].append(i)
    return data, vehicle_dict

def vehicles_to_file(data, vehicle_dict, file_name1, file_name2):
    data.to_csv(file_name1, index=False, header=True)
    file = open(file_name2, 'wb')
    pickle.dump(vehicle_dict, file)
    file.close()

def gen_vehicles():
    data, vehicle_dict = cal_vehicles()
    vehicles_to_file(data, vehicle_dict, 'vehicles_df/vehicles_df.csv', 'vehicle_dict/vehicle_dict.pkl')

# gen_vehicles()