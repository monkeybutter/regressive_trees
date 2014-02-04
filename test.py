import numpy as np


runs = [510, 511, 512, 513, 514, 517, 521]
runs = [514]

a = [1.0, 2.0, 3.0]
b = [2.0, 2.0, 2.0]

nda = np.asarray(a)
ndb = np.sin(np.asarray(b))

print(type(nda[0]))


#print(ndc)

ndc = nda * ndb


print(ndc)

