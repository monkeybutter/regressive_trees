__author__ = 'SmartWombat'

from tree_parallel import Tree
from data.data import Data
from evaluator import evaluate_dataset_rmse
import pickle

airports = ['yssy', 'egll', 'zbaa']

class_vars = ['metar_wind_spd', 'metar_temp', 'metar_rh']

for airport in airports:
    print airport

    for class_var in class_vars:
        print class_var

        cx_bin_number = 5
        for i in range(cx_bin_number):
            print i+1

            test_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_cir_testdf.pick".format(airport, class_var, i+1), "rb"))
            train_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_cir_traindf.pick".format(airport, class_var, i+1), "rb"))
            test_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_testdf.pick".format(airport, class_var, i+1), "rb"))
            train_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_traindf.pick".format(airport, class_var, i+1), "rb"))

            lin_types = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
            cir_types = ['linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

            data_lin = Data(train_df_lin, class_var, lin_types, True)
            tree = Tree()
            node_lin = tree.tree_grower(data_lin, 100)

            data_cir = Data(train_df_cir, class_var, cir_types, True)
            tree = Tree()
            node_cir = tree.tree_grower(data_cir, 100)

            print("RMSE Linear {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'linear', node_lin, test_df_lin)))
            print("RMSE Circular {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'linear', node_cir, test_df_cir)))

