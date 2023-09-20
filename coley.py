import matplotlib.pyplot as plt
import pandas as pd

import Filter


# Old version of coley algorithm
def coley(left, right, steer):
    df_left = pd.read_json(left)
    df_right = pd.read_json(right)
    df_steer = pd.read_json(steer)
    threshold = 1

    [df_left, df_right, df_steer] = Filter.filter_data([df_left, df_right, df_steer], filter_data_band_flag=True,
                                                       ma_to_second_flag=True, limit_to_interval_flag=True, start=83,
                                                       end=138)

    max_accel_formula = lambda x: x[['accel_x', 'accel_y', 'accel_z']].max(axis=1)
    min_accel_formula = lambda x: x[['accel_x', 'accel_y', 'accel_z']].min(axis=1)
    max_gyro_formula = lambda x: x[['gyro_x', 'gyro_y', 'gyro_z']].max(axis=1)
    min_gyro_formula = lambda x: x[['gyro_x', 'gyro_y', 'gyro_z']].min(axis=1)
    accel_range_formula = lambda x: x['max_accel'] - x['min_accel']
    gyro_range_formula = lambda x: x['max_gyro'] - x['min_gyro']
    for data in [df_left, df_right, df_steer]:
        data['max_accel'] = max_accel_formula(data)
        data['min_accel'] = min_accel_formula(data)
        data['max_gyro'] = max_gyro_formula(data)
        data['min_gyro'] = min_gyro_formula(data)
        data['accel_range'] = accel_range_formula(data)
        data['gyro_range'] = gyro_range_formula(data)

    df_left['PR_LN'] = df_left['accel_range'] * df_left['gyro_range']
    df_left['PR_RN'] = df_right['accel_range'] * df_right['gyro_range']
    df_left['PR_S'] = df_steer['accel_range'] * df_steer['gyro_range']
    df_left['PR_L'] = df_left['PR_LN'] - df_left['PR_S']
    df_left['PR_R'] = df_left['PR_RN'] - df_left['PR_S']

    df_left['active_L'] = (df_left['PR_L'] > threshold)
    df_left['active_R'] = (df_left['PR_R'] > threshold)
    df_left['active_L'] = df_left['active_L'].astype(int)
    df_left['active_R'] = df_left['active_R'].astype(int)

    print("HERE:" + str(df_left['active_L'].head()))

    # if right is active, PI = right, else if left is active, PI = left else PI = 0
    df_left['PI'] = df_left['active_R'] * df_left['PR_R'] - df_left['active_L'] * df_left['PR_L']

    ARS = df_left['active_R'].sum()
    ALS = df_left['active_L'].sum()
    df_left['ARSp'] = df_left['active_R'].rolling(240).sum() / 240
    df_left['ALSp'] = df_left['active_L'].rolling(240).sum() / 240
    Total = ARS + ALS
    ARSp = ARS / Total
    ALSp = ALS / Total
    print('ARS: ', ARS)
    print('ALS: ', ALS)
    print('Total: ', Total)
    print('ARSp: ', ARSp)
    print('ALSp: ', ALSp)

    # plot
    df_left['active_R_1s'] = df_left['active_R'].rolling(120).sum()
    df_left['active_L_1s'] = df_left['active_L'].rolling(120).sum()
    plt.plot(df_left['active_R'], label='steer', color='green')
    plt.show()
    # plt.plot(df_left['PR_RN'], label='steer', color='red')
    plt.show()
