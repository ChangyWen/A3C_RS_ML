#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from sys import maxsize
import numpy as np
from global_parameters import VEHICLES_NUMS, REQUEST_NUMS, get_value, MAX_DETOUR_TIME
import copy

def cal_profit(VEHICLES, request_selected, vehicle, current_time):
    DATA = get_value('DATA')
    current_hour = int(current_time / 60)
    profit_matrix = np.zeros(shape=[VEHICLES_NUMS, REQUEST_NUMS]) # N * M
    travel_time = get_value('travel_time')
    fare = get_value('fare')
    for i in range(len(vehicle)):
        for j in range(len(request_selected)):
            ve = vehicle[i]
            re = request_selected[j]
            if re == -1:
                continue
            if travel_time[current_hour][VEHICLES[ve].location][DATA.loc[re, 'PULocationID']] < MAX_DETOUR_TIME and DATA.loc[re, 'passenger_count'] <= VEHICLES[ve].cap - VEHICLES[ve].load:
                cost = (fare[VEHICLES[ve].location][DATA.loc[re, 'PULocationID']] + fare[DATA.loc[re, 'PULocationID']][DATA.loc[re, 'DOLocationID']])* 0.1
                fee = fare[DATA.loc[re, 'PULocationID']][DATA.loc[re, 'DOLocationID']]
                profit_matrix[i][j] = (fee - cost) if fee > cost else 0
    return profit_matrix

def KM_mapping(action, VEHICLES, request_selected, vehicle, current_time): # ?????
    '''
    :param prob_weights: a_prob
    :return: matching final action,"indexes":
    '''
    print('cal_profit begin')
    profit_matrix = cal_profit(VEHICLES, request_selected, vehicle, current_time)
    print('cal_profit end')
    action = action.reshape([1,VEHICLES_NUMS * REQUEST_NUMS])
    action = np.apply_along_axis(lambda x: round(x[0], 2), 0, action)
    action_weights = action.reshape([VEHICLES_NUMS,REQUEST_NUMS])
    km_matrix = profit_matrix * action_weights
    # km_weights = make_cost_matrix(km_matrix, lambda item: (maxsize - item) if item != 0 else DISALLOWED)
    km_weights = make_cost_matrix(km_matrix, lambda item: (400 - item))
    m = Munkres()
    print('km begin')
    indexes = m.compute(km_weights)
    print('km_end')
    print_matrix(profit_matrix, msg='Highers profit through this matrix:')
    total = 0
    temp_indexes = copy.deepcopy(indexes)
    for row, column in temp_indexes:
        value = profit_matrix[row][column]
        if value == 0:
            indexes.remove((row, column))
        total += value
    return indexes, total

# KM_mapping([])