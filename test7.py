__author__ = 'SmartWombat'

from tree_parallel import Tree
from data.data import Data
from evaluator import evaluate_dataset_rmse
import pickle

airports = ['yssy', 'egll', 'zbaa']

class_var = 'metar_wind_dir'

for airport in airports:
    print airport

    cx_bin_number = 5

    for i in range(cx_bin_number):

        test_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_cir_testdf.pick".format(airport, class_var, i+1), "rb"))
        train_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_cir_traindf.pick".format(airport, class_var, i+1), "rb"))
        test_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_testdf.pick".format(airport, class_var, i+1), "rb"))
        train_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_traindf.pick".format(airport, class_var, i+1), "rb"))

        lin_lin_types = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
        cir_lin_types = ['circular', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
        lin_cir_types = ['linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']
        cir_cir_types = ['circular', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

        data_lin = Data(train_df_lin, class_var, lin_lin_types, True)
        tree = Tree()
        node_lin_lin = tree.tree_grower(data_lin, 1000)
        data_cir = Data(train_df_lin, class_var, cir_lin_types, True)
        tree = Tree()
        node_cir_lin = tree.tree_grower(data_cir, 1000)
        data_lin = Data(train_df_cir, class_var, lin_cir_types, True)
        tree = Tree()
        node_lin_cir = tree.tree_grower(data_lin, 1000)
        data_cir = Data(train_df_cir, class_var, cir_cir_types, True)
        tree = Tree()
        node_cir_cir = tree.tree_grower(data_cir, 1000)

        print("RMSE Linear Linear {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'circular', node_lin_lin, test_df_lin)))
        print("RMSE Circular Linear {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'circular', node_cir_lin, test_df_lin)))
        print("RMSE Linear Circular {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'circular', node_lin_cir, test_df_cir)))
        print("RMSE Circular Circular {}: {}".format(i+1, evaluate_dataset_rmse(class_var, 'circular', node_cir_cir, test_df_cir)))

