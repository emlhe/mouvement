import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import Filter


def calculate(left, right, steer, start, end, real_time=False):
    # convert timestamps to seconds
    df_left = pd.read_json(left)
    df_right = pd.read_json(right)
    df_steer = pd.read_json(steer)

    min_angle = 15

    plt.subplot(2,3,1)
    plt.plot(df_left["timestamp"], df_left["gyro_x"])
    plt.title("gauche, gyro_x")
    plt.subplot(2,3,2)
    plt.plot(df_left["timestamp"], df_left["gyro_y"])
    plt.title("gauche, gyro_y")
    plt.subplot(2,3,3)
    plt.plot(df_left["timestamp"], df_left["gyro_z"])
    plt.title("gauche, gyro_z")
    plt.subplot(2,3,4)
    plt.plot(df_right["timestamp"], df_right["gyro_x"])
    plt.title("droit, gyro_x")
    plt.subplot(2,3,5)
    plt.plot(df_right["timestamp"], df_right["gyro_y"])
    plt.title("droit, gyro_y")
    plt.subplot(2,3,6)
    plt.plot(df_right["timestamp"], df_right["gyro_z"])
    plt.title("droit, gyro_z")
    plt.show()

    [df_left, df_right, df_steer] = Filter.filter_datas([df_left, df_right, df_steer], filter_data_band_flag=True,
                                                        ma_to_second_flag=False, limit_to_interval_flag=True,
                                                        start=start,
                                                        end=end)

    # Find all peaks where a peak is a value that is greater than min_angle
    df_left["gyro_x_peaks"] = df_left["gyro_x"].apply(lambda x: x if x > min_angle else 0)
    df_right["gyro_x_peaks"] = df_right["gyro_x"].apply(lambda x: x if x > min_angle else 0)
    df_left["gyro_y_peaks"] = df_left["gyro_y"].apply(lambda x: x if x > min_angle else 0)
    df_right["gyro_y_peaks"] = df_right["gyro_y"].apply(lambda x: x if x > min_angle else 0)
    df_left["gyro_z_peaks"] = df_left["gyro_z"].apply(lambda x: x if x > min_angle else 0)
    df_right["gyro_z_peaks"] = df_right["gyro_z"].apply(lambda x: x if x > min_angle else 0)
    df_steer["gyro_x_peaks"] = df_steer["gyro_x"].apply(lambda x: x if x > min_angle else 0)
    df_steer["gyro_y_peaks"] = df_steer["gyro_y"].apply(lambda x: x if x > min_angle else 0)
    df_steer["gyro_z_peaks"] = df_steer["gyro_z"].apply(lambda x: x if x > min_angle else 0)

    df_left.info()
    df_right.info()
    df_steer.info()

    plt.subplot(3,2,1)
    plt.plot(df_left["timestamp"], df_left["gyro_x"])
    plt.title("gauche, gyro_x")
    plt.subplot(3,2,2)
    plt.plot(df_left["timestamp"], df_left["gyro_x_peaks"])
    plt.title("gauche, gyro_x, peaks > "+ str(min_angle))
    plt.subplot(3,2,3)
    plt.plot(df_left["timestamp"], df_left["gyro_y"])
    plt.title("gauche, gyro_y")
    plt.subplot(3,2,4)
    plt.plot(df_left["timestamp"], df_left["gyro_y_peaks"])
    plt.title("gauche, gyro_y, peaks > "+ str(min_angle))
    plt.subplot(3,2,5)
    plt.plot(df_left["timestamp"], df_left["gyro_z"])
    plt.title("gauche, gyro_z")
    plt.subplot(3,2,6)
    plt.plot(df_left["timestamp"], df_left["gyro_z_peaks"])
    plt.title("gauche, gyro_z, peaks > "+ str(min_angle))
    plt.show()

    plt.subplot(3,2,1)
    plt.plot(df_right["timestamp"], df_right["gyro_x"])
    plt.title("droit, gyro_x")
    plt.subplot(3,2,2)
    plt.plot(df_right["timestamp"], df_right["gyro_x_peaks"])
    plt.title("droit, gyro_x, peaks > "+ str(min_angle))
    plt.subplot(3,2,3)
    plt.plot(df_right["timestamp"], df_right["gyro_y"])
    plt.title("droit, gyro_y")
    plt.subplot(3,2,4)
    plt.plot(df_right["timestamp"], df_right["gyro_y_peaks"])
    plt.title("droit, gyro_y, peaks > "+ str(min_angle))
    plt.subplot(3,2,5)
    plt.plot(df_right["timestamp"], df_right["gyro_z"])
    plt.title("droit, gyro_z")
    plt.subplot(3,2,6)
    plt.plot(df_right["timestamp"], df_right["gyro_z_peaks"])
    plt.title("droit, gyro_z, peaks > "+ str(min_angle))
    plt.show()


    df_res = calculate_total(df_left, df_right, df_steer) if real_time else calculate_real_time(df_left, df_right,
                                                                                                df_steer)
    # Count all the moment of activity in the data and divide it by the frequency
    activity_count_left = df_res["mono_left"].sum() / 128
    activity_count_right = df_res["mono_right"].sum() / 128
    activity_count_both = df_res["bi"].sum() / 128
    df_res['timestamp'] = df_res['timestamp'].apply(lambda x: x - start)

    # Plotting
    go_left = go.Scatter(x=df_res['timestamp'], y=df_res["mono_left"],
                         name=str(100 * activity_count_left / (end - start)) + "% -> LW", line=dict(width=3))
    go_right = go.Scatter(x=df_res['timestamp'], y=df_res["mono_right"], name=str(
        100 * activity_count_right / (end - start)) + "% -> RW", line=dict(width=3))
    go_bi = go.Scatter(x=df_res['timestamp'], y=df_res["bi"],
                       name=str(100 * activity_count_both / (end - start)) + "% -> BI", line=dict(width=5))

    # fig = go.Figure()
    # fig.add_trace(go_left)
    # fig.add_trace(go_right)
    # fig.add_trace(go_bi)
    # fig.show()


def calculate_total(df_left, df_right, df_steer):
    threshold_left = min(df_left["gyro_x_peaks"].mean(), df_left["gyro_y_peaks"].mean(), df_left["gyro_z_peaks"].mean())
    threshold_right = min(df_right["gyro_x_peaks"].mean(), df_right["gyro_y_peaks"].mean(),
                          df_right["gyro_z_peaks"].mean())
    threshold_steer = min(df_steer["gyro_x_peaks"].mean(), df_steer["gyro_y_peaks"].mean(),
                          df_steer["gyro_z_peaks"].mean())

    df_left["activity"] = (
            df_left[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > threshold_left).astype(int)
    df_right["activity"] = (
            df_right[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > threshold_right).astype(int)
    df_steer["activity"] = (
            df_steer[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > threshold_steer).astype(int)

    df_left["activity_ma_256"] = df_left["activity"].rolling(window=256, min_periods=1).mean()
    df_right["activity_ma_256"] = df_right["activity"].rolling(window=256, min_periods=1).mean()
    df_steer["activity_ma_256"] = df_steer["activity"].rolling(window=256, min_periods=1).mean()

    df_left["supposed_activity"] = df_left["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)
    df_right["supposed_activity"] = df_right["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)
    df_steer["supposed_activity"] = df_steer["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)

    df_left['supposed_activity__left_and_right'] = df_left['supposed_activity'] & df_right[
        'supposed_activity']

    df_res = pd.DataFrame()

    df_res["timestamp"] = df_left["timestamp"]

    df_res["bi"] = df_left['supposed_activity__left_and_right']

    df_res["mono_left"] = df_left['supposed_activity'] > df_res['bi']
    df_res["mono_left"] = df_res["left"].astype(int)
    df_res["mono_right"] = df_right['supposed_activity'] > df_res['bi']
    df_res["mono_right"] = df_res["right"].astype(int)

    return df_res


def calculate_real_time(df_left, df_right, df_steer):
    # For every moment, calculate the mean of all the values before
    df_left['gyro_x_peaks'] = df_left['gyro_x_peaks'].expanding().mean()
    df_right['gyro_x_peaks'] = df_right['gyro_x_peaks'].expanding().mean()
    df_steer['gyro_x_peaks'] = df_steer['gyro_x_peaks'].expanding().mean()
    df_left['gyro_y_peaks'] = df_left['gyro_y_peaks'].expanding().mean()
    df_right['gyro_y_peaks'] = df_right['gyro_y_peaks'].expanding().mean()
    df_steer['gyro_y_peaks'] = df_steer['gyro_y_peaks'].expanding().mean()
    df_left['gyro_z_peaks'] = df_left['gyro_z_peaks'].expanding().mean()
    df_right['gyro_z_peaks'] = df_right['gyro_z_peaks'].expanding().mean()
    df_steer['gyro_z_peaks'] = df_steer['gyro_z_peaks'].expanding().mean()

    plt.subplot(2,3,1)
    plt.plot(df_left["timestamp"], df_left["gyro_x_peaks"])
    plt.title("gauche, gyro_x")
    plt.subplot(2,3,2)
    plt.plot(df_left["timestamp"], df_left["gyro_y_peaks"])
    plt.title("gauche, gyro_y")
    plt.subplot(2,3,3)
    plt.plot(df_left["timestamp"], df_left["gyro_z_peaks"])
    plt.title("gauche, gyro_z")
    plt.subplot(2,3,4)
    plt.plot(df_right["timestamp"], df_right["gyro_x_peaks"])
    plt.title("droite, gyro_x")
    plt.subplot(2,3,5)
    plt.plot(df_right["timestamp"], df_right["gyro_y_peaks"])
    plt.title("droite, gyro_y")
    plt.subplot(2,3,6)
    plt.plot(df_right["timestamp"], df_right["gyro_z_peaks"])
    plt.title("droite, gyro_z")
    plt.show()

    # Pour chaque capteur : seuil = minimum des 3 gyro 
    df_left['threshold'] = df_left[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].min(
        axis=1)
    df_right['threshold'] = df_right[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].min(
        axis=1)
    df_steer['threshold'] = df_steer[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].min(
        axis=1)

    plt.subplot(2,1,1)
    plt.plot(df_left["timestamp"], df_left["threshold"])
    plt.title("seuil gauche")
    plt.subplot(2,1,2)
    plt.plot(df_right["timestamp"], df_right["threshold"])
    plt.title("seuil droite")
    plt.show()

    # Activité = max des 3 gyro > threshold 
    df_left["activity"] = (df_left[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > df_left[
        "threshold"]).astype(int)
    df_right["activity"] = (df_right[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > df_right[
        "threshold"]).astype(int)
    df_steer["activity"] = (df_steer[['gyro_x_peaks', 'gyro_y_peaks', 'gyro_z_peaks']].max(axis=1) > df_steer[
        "threshold"]).astype(int)

    plt.subplot(2,1,1)
    plt.plot(df_left["timestamp"], df_left["activity"])
    plt.title("activity gauche")
    plt.subplot(2,1,2)
    plt.plot(df_right["timestamp"], df_right["activity"])
    plt.title("activity droite")
    plt.show()

    # Moyenne de toutes les activités précédentes
    df_left["activity_ma_256"] = df_left["activity"].rolling(window=256, min_periods=1).mean()
    df_right["activity_ma_256"] = df_right["activity"].rolling(window=256, min_periods=1).mean()
    df_steer["activity_ma_256"] = df_steer["activity"].rolling(window=256, min_periods=1).mean()

    plt.subplot(2,1,1)
    plt.plot(df_left["timestamp"], df_left["activity_ma_256"])
    plt.title("moyenne activity gauche")
    plt.subplot(2,1,2)
    plt.plot(df_right["timestamp"], df_right["activity_ma_256"])
    plt.title("moyenne activity droite")
    plt.show()

    # Si activité, 1, sinon 0
    df_left["supposed_activity"] = df_left["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)
    df_right["supposed_activity"] = df_right["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)
    df_steer["supposed_activity"] = df_steer["activity_ma_256"].apply(lambda x: 1 if x > 0.2 else 0)

    plt.subplot(2,1,1)
    plt.plot(df_left["timestamp"], df_left["supposed_activity"])
    plt.title("supposed activity gauche")
    plt.subplot(2,1,2)
    plt.plot(df_right["timestamp"], df_right["supposed_activity"])
    plt.title("supposed activity droite")
    plt.show()

    # Activité bimanuelle si droite et gauche à 1 
    df_left['supposed_activity__left_and_right'] = df_left['supposed_activity'] & df_right[
        'supposed_activity']

    df_res = pd.DataFrame()
    df_left.info()

    df_res["timestamp"] = df_left["timestamp"]

    # Activité bimanuelle = activité à droite & à gauche
    df_res["bi"] = df_left['supposed_activity__left_and_right']

    # Activité gauche si activité gauche > activité bimanuelle
    df_res["mono_left"] = df_left['supposed_activity'] > df_res['bi']
    df_res["mono_left"] = df_res["mono_left"].astype(int)
    # Activité droite si activité droite > activité bimanuelle
    df_res["mono_right"] = df_right['supposed_activity'] > df_res['bi']
    df_res["mono_right"] = df_res["mono_right"].astype(int)

    plt.subplot(1,3,1)
    plt.plot(df_left["timestamp"], df_res["mono_left"])
    plt.title("mono activity gauche")
    plt.subplot(1,3,2)
    plt.plot(df_right["timestamp"], df_res["mono_left"])
    plt.title("mono activity droite")
    plt.subplot(1,3,3)
    plt.plot(df_right["timestamp"], df_res["bi"])
    plt.title("activity bimanuelle")
    plt.show()

    return df_res
