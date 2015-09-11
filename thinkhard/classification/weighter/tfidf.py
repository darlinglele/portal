from math import log
from decimal import *


class TfIdf():

    def __init__(self, feature_dict, cate_dict):
        self.feature_dict = feature_dict
        self.cate_dict = cate_dict
        self.doc_total = sum([x for x in self.cate_dict.itervalues()])
        self.h = self.h()    

    def get_weight(self, f):
        return 0

    