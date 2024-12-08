from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values, get_time_domain_features, \
    get_geometrical_features, get_frequency_domain_features, get_csi_cvi_features, get_poincare_plot_features, \
    get_sampen
from hrvanalysis import plot_psd, plot_poincare
import matplotlib.pyplot as plt


def preprocessRR(rawRRList):
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rawRRList,
                                                    low_rri=200, high_rri=2000)
    interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                       interpolation_method="linear")
    nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
    interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)
    return interpolated_nn_intervals


def featureRRplots(nn_intervals_list):
    plot_psd(nn_intervals_list, method="welch")
    plot_psd(nn_intervals_list, method="lomb")
    plot_poincare(nn_intervals_list, plot_sd_features=True)

def rrFeatureExtraction(nn_intervals_list):
    print(nn_intervals_list)
    time_domain_features = get_time_domain_features(nn_intervals_list)
    print(time_domain_features)

    geometrical_features = get_geometrical_features(nn_intervals_list)
    print(geometrical_features)

    frequency_domain_features = get_frequency_domain_features(nn_intervals_list)
    print(frequency_domain_features)

    nonlin_features = get_csi_cvi_features(nn_intervals_list)
    print(nonlin_features)

    poincare_plot_features = get_poincare_plot_features(nn_intervals_list)
    print("!!!!!!!!!")
    print(poincare_plot_features)

    #sampen = get_sampen(nn_intervals_list)
    #print(sampen)

