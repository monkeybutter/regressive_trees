__author__ = 'SmartWombat'

import pandas
from tree_parallel import Tree
from data.data import Data


df = pandas.read_csv("./web/static/data/YSSY.csv")
#print df.head(5)
#df.gfs_wind_dir = int(df.gfs_wind_dir/10) * 10
df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x/10) *  10).head()

#print df.head(5)


print df.shape

class_var = 'metar_temp'
var_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']



data = Data(df, class_var, var_types, True)
tree = Tree()
node = tree.tree_grower(data, 500)

#tree.tree_runner(node, "O")
print tree.tree_to_dict(node, "O")

