import numpy as np
from scipy.signal import ellipord, ellip, sosfilt

f = 128
fn = f / 2
Rp = 1
Rs = 50
Wp = np.divide([0.25, 2.5], fn)
Ws = np.divide([0.1, 3], fn)
N, Wn = ellipord(Wp, Ws, Rp, Rs)
sos = ellip(N, Rp, Rs, Wp, btype='bandpass', analog=False, output='sos')


def filter_data_band(data):
    data['accel_x'] = sosfilt(sos, data['accel_x'])
    data['accel_y'] = sosfilt(sos, data['accel_y'])
    data['accel_z'] = sosfilt(sos, data['accel_z'])
    data['gyro_x'] = sosfilt(sos, data['gyro_x'])
    data['gyro_y'] = sosfilt(sos, data['gyro_y'])
    data['gyro_z'] = sosfilt(sos, data['gyro_z'])
    return data


def ma_to_second(data):
    data['accel_x'] = data['accel_x'].rolling(window=f, min_periods=1).mean()
    data['accel_y'] = data['accel_y'].rolling(window=f, min_periods=1).mean()
    data['accel_z'] = data['accel_z'].rolling(window=f, min_periods=1).mean()
    data['gyro_x'] = data['gyro_x'].rolling(window=f, min_periods=1).mean()
    data['gyro_y'] = data['gyro_y'].rolling(window=f, min_periods=1).mean()
    data['gyro_z'] = data['gyro_z'].rolling(window=f, min_periods=1).mean()

    return data


def limit_to_interval(data, start, end):
    data = data[data['timestamp'] > start]
    data = data[data['timestamp'] < end]
    return data


def filter_data(data, filter_data_band_flag=False, ma_to_second_flag=False, limit_to_interval_flag=False, start=0,
                end=0):
    if limit_to_interval_flag:
        data = limit_to_interval(data, start, end)
    if filter_data_band_flag:
        data = filter_data_band(data)
    if ma_to_second_flag:
        data = ma_to_second(data)
    return data


def filter_datas(datas, filter_data_band_flag=False, ma_to_second_flag=False, limit_to_interval_flag=False, start=0,
                 end=0):
    for i in range(len(datas)):
        datas[i] = filter_data(datas[i], filter_data_band_flag, ma_to_second_flag, limit_to_interval_flag, start, end)
    return datas
