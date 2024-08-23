#!/usr/bin/env python3
import sys
from os.path import dirname, abspath

cmsbot_dir = None
if __file__:
    cmsbot_dir = dirname(dirname(abspath(__file__)))
else:
    cmsbot_dir = dirname(dirname(abspath(sys.argv[0])))
sys.path.insert(0, cmsbot_dir)

from es_utils import get_indexes, open_index, find_indexes
from cmsutils import epoch2week
from time import time

cur_week = int(epoch2week(time(), 1))

for i in sys.argv[1:]:
    idxs = find_indexes(i)
    if not "close" in idxs:
        continue
    for ix in sorted(idxs["close"]):
        print("Opening ", ix)
        open_index(ix)
        print(get_indexes(ix))
