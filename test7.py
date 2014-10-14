__author__ = 'SmartWombat'

from tree_parallel import Tree
from data.data import Data
from evaluator import evaluate_dataset_rmse
import pickle

airports = ['yssy', 'egll', 'zbaa']

gfs_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_dir', 'gfs_wind_spd', 'time', 'date']

gfs_types = list()
gfs_types.append({'name': 'circular', 'types': ['linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']})
gfs_types.append({'name': 'linear', 'types': ['linear'] * 7})

class_var = 'metar_wind_dir'
class_var_types = ['circular', 'linear']

for airport in airports:
    print airport

    cx_bin_number = 5

    for i in range(cx_bin_number):

        test_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_testdf.pick".format(airport, class_var, i+1), "rb"))
        train_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_traindf.pick".format(airport, class_var, i+1), "rb"))
        test_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_testdf.pick".format(airport, class_var, i+1), "rb"))
        train_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/{}_{}_cx{}_lin_traindf.pick".format(airport, class_var, i+1), "rb"))

        lin_types = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
        cir_types = ['circular', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']

        print("linear")
        data_lin = Data(train_df_lin, class_var, lin_types, True)
        tree = Tree()
        node_lin = tree.tree_grower(data_lin, 100)
        print("circular")
        data_cir = Data(train_df_cir, class_var, cir_types, True)
        tree = Tree()
        node_cir = tree.tree_grower(data_cir, 100)

        print("RMSE Linear {}: {}\n".format(i+1, evaluate_dataset_rmse(class_var, node_lin, test_df_lin)))
        print("RMSE Circular {}: {}\n".format(i+1, evaluate_dataset_rmse(class_var, node_cir, test_df_cir)))

