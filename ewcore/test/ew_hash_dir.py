from os import listdir
from os.path import isfile, join

from ewcore.test.ew_hash_file import ew_file

mypath="/Users/casatta/Downloads/blockchain corso/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)

for f in onlyfiles:
    fname = join(mypath,f)
    fd = open(fname, 'rb')
    ew_file(fd)

