import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import log

import Filter

from PandaTools import apply_to_dataframes

CONV = 0.001664
AC_threshold = 2


def calculate(left, right, steer, result_as_csv=False, data_to_plot=None):
    # convert timestamps to seconds
    df_left = pd.read_json(left)
    df_right = pd.read_json(right)
    df_steer = pd.read_json(steer)

    [df_left, df_right, df_steer] = Filter.filter_datas([df_left, df_right, df_steer], filter_data_band_flag=True,
                                                        ma_to_second_flag=False, limit_to_interval_flag=True, start=60,
                                                        end=220)

    [df_left, df_right, df_steer] = apply_to_dataframes([df_left, df_right, df_steer],
                                                        lambda x: np.sqrt(np.square(
                                                            x['accel_x'] / CONV) + np.square(
                                                            x['accel_y'] / CONV) + np.square(
                                                            x['accel_z'] / CONV)), "AC")

    df_left["AC_peaks"] = df_left["AC"].apply(lambda x: x if x > AC_threshold else 0)
    df_right["AC_peaks"] = df_right["AC"].apply(lambda x: x if x > AC_threshold else 0)
    df_steer["AC_peaks"] = df_steer["AC"].apply(lambda x: x if x > AC_threshold else 0)

    treshold_left = df_left["AC_peaks"].mean()
    treshold_right = df_right["AC_peaks"].mean()
    treshold_steer = df_steer["AC_peaks"].mean()

    df_left["activity"] = df_left["AC_peaks"].apply(lambda x: 1 if x > treshold_left else 0)
    df_right["activity"] = df_right["AC_peaks"].apply(lambda x: 1 if x > treshold_right else 0)
    df_steer["activity"] = df_steer["AC_peaks"].apply(lambda x: 1 if x > treshold_steer else 0)

    df_left["activity_ma_128"] = df_left["activity"].rolling(window=256, min_periods=1).mean()
    df_right["activity_ma_128"] = df_right["activity"].rolling(window=256, min_periods=1).mean()
    df_steer["activity_ma_128"] = df_steer["activity"].rolling(window=256, min_periods=1).mean()

    df_left["supposed_activity"] = df_left["activity_ma_128"].apply(lambda x: 1 if x > 0.5 else 0)
    df_right["supposed_activity"] = df_right["activity_ma_128"].apply(lambda x: 1 if x > 0.5 else 0)
    df_steer["supposed_activity"] = df_steer["activity_ma_128"].apply(lambda x: 1 if x > 0.5 else 0)

    activity_count_left = df_left["supposed_activity"].sum()
    activity_count_right = df_right["supposed_activity"].sum()
    activity_count_steer = df_steer["supposed_activity"].sum()
    print("activity_count_left: " + str(activity_count_left / 128))
    print("activity_count_right: " + str(activity_count_right / 128))
    print("activity_count_steer: " + str(activity_count_steer / 128))

    # plot
    plt.plot(df_left["timestamp"], df_left['supposed_activity'], label="supposed_activity")
    plt.plot(df_right["timestamp"], df_right['supposed_activity'], label="supposed_activity")
    plt.show()

    dom_mean = df_right['AC'].mean()
    non_dom_mean = df_left['AC'].mean()
    steer_mean = df_steer['AC'].mean()

    dom_median = df_right['AC'].median()
    non_dom_median = df_left['AC'].median()
    steer_median = df_steer['AC'].median()

    bilateral_magnitude_mean = dom_mean + non_dom_mean
    bilateral_magnitude_median = dom_median + non_dom_median
    df_left['log_ratio'] = log(1 + df_left['AC']) - log(1 + df_right['AC'])
    df_left['log_ratio'] = log(1 + df_left['AC']) - log(1 + df_right['AC'])

    log_ratio_mean = df_left['log_ratio'].mean()
    log_ratio_median = df_left['log_ratio'].median()

    df_left['MV'] = df_left['AC'] > AC_threshold
    df_right['MV'] = df_right['AC'] > AC_threshold
    df_steer['MV'] = df_steer['AC'] > AC_threshold

    MAUI = ((df_left['MV'] ^ 1) * df_left['AC']).sum() / ((df_right['MV'] ^ 1) * df_right['AC']).sum()  # Broken
    BAUI = (df_left['MV'] * df_left['AC']).sum() / (df_right['MV'] * df_right['AC']).sum()

    non_dom_activity = df_left['MV'].sum()
    dom_activity = df_right['MV'].sum()
    steer_activity = df_steer['MV'].sum()

    dom_sed = (df_right['MV'] ^ 1).sum()
    non_dom_sed = (df_left['MV'] ^ 1).sum()
    steer_sed = (df_steer['MV'] ^ 1).sum()

    dom_unilateral = (df_right['MV'] * (df_left['MV'] ^ 1)).sum()
    non_dom_unilateral = (df_left['MV'] * (df_right['MV'] ^ 1)).sum()

    bilateral = (df_right['MV'] * df_left['MV']).sum()

    use_ratio = non_dom_activity / dom_activity

    if result_as_csv:
        data = [dom_mean, non_dom_mean, steer_mean, dom_median, non_dom_median, steer_median, bilateral_magnitude_mean,
                bilateral_magnitude_median, log_ratio_mean, log_ratio_median, MAUI, BAUI, non_dom_activity,
                dom_activity,
                steer_activity, dom_sed, non_dom_sed, steer_sed, dom_unilateral, non_dom_unilateral, bilateral,
                use_ratio]
        data_str = [str(x) for x in data]
        csv_line = ",".join(data_str)
        csv_line = csv_line + "\n"
        return csv_line

    if data_to_plot is not None:
        for i in range(0, len(data_to_plot)):
            plt.plot(df_left[data_to_plot[i]])
            plt.plot(df_right[data_to_plot[i]])
            plt.plot(df_steer[data_to_plot[i]])
            plt.legend(['Left', 'Right', 'Steer'])
            plt.title(data_to_plot[i])
            plt.show()
