__author__ = 'SmartWombat'

from tree_parallel import Tree, tree_to_dict
from data.data import Data
from evaluator import evaluate_dataset_rmse
import pickle


test_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/test_cir_df.pick", "rb"))
train_df_cir = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/train_cir_df.pick", "rb"))
test_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/test_cir_df.pick", "rb"))
train_df_lin = pickle.load(open("/home/roz016/Dropbox/Data for Tree/Results/train_cir_df.pick", "rb"))

lin_types = ['linear', 'linear']
cir_types = ['circular', 'linear']

print("linear")
data_lin = Data(train_df_lin, 'dir', lin_types, True)
tree = Tree()
node_lin = tree.tree_grower(data_lin, 200)

print("circular")
data_cir = Data(train_df_cir, 'dir', cir_types, True)
tree = Tree()
node_cir = tree.tree_grower(data_cir, 200)


print("RMSE Linear: {}".format(evaluate_dataset_rmse('dir', 'circular', node_lin, test_df_lin)))
print("RMSE Circular: {}".format(evaluate_dataset_rmse('dir', 'circular', node_cir, test_df_cir)))

print(tree_to_dict(node_lin, "O"))
print(tree_to_dict(node_cir, "O"))
