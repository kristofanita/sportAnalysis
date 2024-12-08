import pandas as pd
import numpy as np
import zipfile
import warnings

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from mlxtend.plotting import plot_decision_regions

filename="gust_boxing.zip"
df_raw_left=pd.read_excel(zipfile.ZipFile(filename).open("GUST_boxing_classification_data/Raw_sensor_training_data.xlsx"),sheet_name="Left wrist")
df_raw_right=pd.read_excel(zipfile.ZipFile(filename).open("GUST_boxing_classification_data/Raw_sensor_training_data.xlsx"),sheet_name="Right wrist")
df_raw_t3=pd.read_excel(zipfile.ZipFile(filename).open("GUST_boxing_classification_data/Raw_sensor_training_data.xlsx"),sheet_name="Upper back (T3)")

df_raw_left.drop('Sample_rate (Hz)', axis='columns', inplace=True)
df_raw_left = df_raw_left.dropna()
df_raw_right.drop('Sample_rate (Hz)', axis='columns', inplace=True)
df_raw_right = df_raw_right.dropna()

df_raw_t3.drop('Sample_rate (Hz)', axis='columns', inplace=True)
df_raw_t3.dropna()

df_types_from_video=pd.read_excel(zipfile.ZipFile(filename).open("GUST_boxing_classification_data/Punch_orders_video_analysis.xlsx"))

all3 = [df_raw_left, df_raw_right, df_raw_t3]
def calc_features(df_raw):
  features={}
  instances = pd.DataFrame(columns=["Ax_mean","Ax_std","Ax_min","Ax_max","Ax_kurtosis","Ax_skew","Ay_mean","Ay_std","Ay_min","Ay_max","Ay_kurtosis","Ay_skew","Az_mean","Az_std","Az_min","Az_max","Az_kurtosis","Gx_mean","Gx_std","Gx_min","Gx_max","Gx_kurtosis","Gy_mean","Gy_std","Gy_min","Gy_max","Gy_kurtosis","Gz_mean","Gz_std","Gz_min","Gz_max","Gz_kurtosis","Roll_mean","Roll_std","Roll_min","Roll_max","Roll_kurtosis","Pitch_mean","Pitch_std","Pitch_min","Pitch_max","Pitch_kurtosis","Yaw_mean","Yaw_std","Yaw_min","Yaw_max","Yaw_kurtosis"])
  for j in range(250):
    for i in range(299):
      start = i*299
      end = (i+1)*299
      features["Ax_mean"]=df_raw["Accel_x (g)"].iloc[start:end].mean()
      features["Ax_std"]=df_raw["Accel_x (g)"].iloc[start:end].std()
      features["Ax_min"]=df_raw["Accel_x (g)"].iloc[start:end].min()
      features["Ax_max"]=df_raw["Accel_x (g)"].iloc[start:end].max()
      features["Ax_kurtosis"]=df_raw["Accel_x (g)"].iloc[start:end].kurtosis()
      features["Ax_skew"]=df_raw["Accel_x (g)"].iloc[start:end].skew()

      features["Ay_mean"]=df_raw["Accel_y (g)"].iloc[start:end].mean()
      features["Ay_std"]=df_raw["Accel_y (g)"].iloc[start:end].std()
      features["Ay_min"]=df_raw["Accel_y (g)"].iloc[start:end].min()
      features["Ay_max"]=df_raw["Accel_y (g)"].iloc[start:end].max()
      features["Ay_kurtosis"]=df_raw["Accel_y (g)"].iloc[start:end].kurtosis()
      features["Ay_skew"]=df_raw["Accel_y (g)"].iloc[start:end].skew()

      features["Az_mean"]=df_raw["Accel_z (g)"].iloc[start:end].mean()
      features["Az_std"]=df_raw["Accel_z (g)"].iloc[start:end].std()
      features["Az_min"]=df_raw["Accel_z (g)"].iloc[start:end].min()
      features["Az_max"]=df_raw["Accel_z (g)"].iloc[start:end].max()
      features["Az_kurtosis"]=df_raw["Accel_z (g)"].iloc[start:end].kurtosis()
      features["Az_skew"]=df_raw["Accel_z (g)"].iloc[start:end].skew()

      features["Gx_mean"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].mean()
      features["Gx_std"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].std()
      features["Gx_min"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].min()
      features["Gx_max"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].max()
      features["Gx_kurtosis"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].kurtosis()
      features["Gx_skew"]=df_raw["Gyro_x (deg/s)"].iloc[start:end].skew()

      features["Gy_mean"]=df_raw["Gyro_y (deg/s"].iloc[start:end].mean()
      features["Gy_std"]=df_raw["Gyro_y (deg/s"].iloc[start:end].std()
      features["Gy_min"]=df_raw["Gyro_y (deg/s"].iloc[start:end].min()
      features["Gy_max"]=df_raw["Gyro_y (deg/s"].iloc[start:end].max()
      features["Gy_kurtosis"]=df_raw["Gyro_y (deg/s"].iloc[start:end].kurtosis()
      features["Gy_skew"]=df_raw["Gyro_y (deg/s"].iloc[start:end].skew()

      features["Gz_mean"]=df_raw["Gyro_z (deg/s"].iloc[start:end].mean()
      features["Gz_std"]=df_raw["Gyro_z (deg/s"].iloc[start:end].std()
      features["Gz_min"]=df_raw["Gyro_z (deg/s"].iloc[start:end].min()
      features["Gz_max"]=df_raw["Gyro_z (deg/s"].iloc[start:end].max()
      features["Gz_kurtosis"]=df_raw["Gyro_z (deg/s"].iloc[start:end].kurtosis()
      features["Gz_skew"]=df_raw["Gyro_z (deg/s"].iloc[start:end].skew()

      features["Roll_mean"]=df_raw["Roll (rad)"].iloc[start:end].mean()
      features["Roll_std"]=df_raw["Roll (rad)"].iloc[start:end].std()
      features["Roll_min"]=df_raw["Roll (rad)"].iloc[start:end].min()
      features["Roll_max"]=df_raw["Roll (rad)"].iloc[start:end].max()
      features["Roll_kurtosis"]=df_raw["Roll (rad)"].iloc[start:end].kurtosis()
      features["Roll_skew"]=df_raw["Roll (rad)"].iloc[start:end].skew()

      features["Pitch_mean"]=df_raw["Pitch (rad)"].iloc[start:end].mean()
      features["Pitch_std"]=df_raw["Pitch (rad)"].iloc[start:end].std()
      features["Pitch_min"]=df_raw["Pitch (rad)"].iloc[start:end].min()
      features["Pitch_max"]=df_raw["Pitch (rad)"].iloc[start:end].max()
      features["Pitch_kurtosis"]=df_raw["Pitch (rad)"].iloc[start:end].kurtosis()
      features["Pitch_skew"]=df_raw["Pitch (rad)"].iloc[start:end].skew()

      features["Yaw_mean"]=df_raw["Yaw (rad)"].iloc[start:end].mean()
      features["Yaw_std"]=df_raw["Yaw (rad)"].iloc[start:end].std()
      features["Yaw_min"]=df_raw["Yaw (rad)"].iloc[start:end].min()
      features["Yaw_max"]=df_raw["Yaw (rad)"].iloc[start:end].max()
      features["Yaw_kurtosis"]=df_raw["Yaw (rad)"].iloc[start:end].kurtosis()
      features["Yaw_skew"]=df_raw["Yaw (rad)"].iloc[start:end].skew()
    instances.loc[j] = features
  return instances


f1 = calc_features(df_raw_left)
f1.to_csv('featuresLeft.csv')
f2 = calc_features(df_raw_right)
f2.to_csv('featuresRight.csv')
f3 = calc_features(df_raw_t3)
f3.to_csv('featuresT3.csv')

joined1 = pd.merge(f1, f2, left_index=True, right_index=True)
inputData = pd.merge(joined1, f3, left_index=True, right_index=True)
inputData = inputData.dropna()
inputData=inputData.drop(inputData.columns[[0]],axis = 1)
inputData.drop(columns=['Unnamed: 0_y', 'Unnamed: 0'], inplace=True)

inputData.to_csv('box_inputs.csv')


