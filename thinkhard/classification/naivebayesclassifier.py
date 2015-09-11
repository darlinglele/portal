# encoding=utf-8
import numpy
import pickle
import jieba
import os
from decimal import *
from time import time
from collections import Counter
import re
from math import log
from weighter.informationgain import InformationGain

class NaiveBayesClassifier():

    def __init__(self, tokenizer=None, stop_words=None):
        self.tokenizer = tokenizer        
        self.features = {}        
        self.categories = {}
        self.cached = {'feature_prob': {}, 'features': {}}

    def fit(self, data, encoding='utf-8'):
        for root, dirs, files in os.walk(data, True):
            for name in files:
                if root.startswith('.') or name.startswith('.'):
                    continue                                   
                category = root.split('/')[-1]                                
                print root.encode('utf-8'),name.encode('utf-8')
                text = open(os.path.join(root,name)).read().decode(encoding)                
                features = self.tokenizer(text)
                for feature in features:
                    self.features.setdefault(feature, {})                    
                    self.features[feature].setdefault(category, 0)
                    self.features[feature][category] += 1
                self.categories.setdefault(category, 0)
                self.categories[category] += 1

    def reduce(self, max_size=10000, weighter=InformationGain):        
        start = time()
        weighter = weighter(self.features, self.categories)
        for f in self.features:
            self.features[f]['weight'] = weighter.get_weight(f)
        reduced_features = sorted(
            [x for x in self.features.items()], key=lambda x: x[1]['weight'], reverse=True)[0:max_size]
        self.reduced_features = {x[0]: x[1] for x in reduced_features}
        print 'reducing completed, costs %0.2f secs' % (time() - start)

    def dump(self, file):
        print 'dumping the raw features to file ', file
        start = time()
        data = {'features': self.features, 'categories': self.categories}
        output = open(file, 'wb')
        pickle.dump(data, output)
        output.close()
        print 'dumping completed costs %0.2f secs' % (time() - start)

    def load(self, file):
        print 'loading raw features from', file, '...'
        start = time()
        input = open(file, 'rb')
        data = pickle.load(input)
        input.close()
        self.features = data['features']
        self.categories = data['categories']
        print 'loading raw features completed, costs %0.2f secs' % (time() - start)
    
    def predict(self, text):
        return sorted([(x, self.posterior_prob(x,text)) for x in self.categories], key=lambda x: x[1], reverse=True)[0][0]

    def posterior_prob(self, category, text):
        if text == None:
            raise Exception('cached_id and text should not both None')
        cached_id =  hash(text)
        if cached_id in self.cached['features']:            
            features = self.cached['features'][cached_id]
        else:            
            features = self.tokenizer(text)
            self.cached['features'] = {cached_id: features}

        return self.likelihood(features, category) * self.prior_prob(category)

    def prior_prob(self, category):
        return float(self.categories.get(category, 0.0)) / sum(self.categories.itervalues())

    #特征向量在类别中的条件概率分布，参数的极大似然估计是基于特征独立性假设
    def likelihood(self, features, category):
        doc_prob = 1.0
        for feature in features:
            if feature in self.reduced_features:
                doc_prob *= self.feature_prob(feature, category)
        return doc_prob

    def feature_prob(self, feature, category, weight=1, alpha=0.5):
        if feature + category in self.cached['feature_prob']:
            return self.cached['feature_prob'][feature + category]
        basic_feature_prob = 0.0
        cf_dict = self.reduced_features[feature]
        cf_sum = sum(cf_dict.itervalues())
        if category in cf_dict:
            basic_feature_prob = float(
                cf_dict[category]) / self.categories[category]
        feature_prob = (
            weight * alpha + cf_sum * basic_feature_prob) / (weight + cf_sum)
        self.cached['feature_prob'][feature + category] = feature_prob
        return feature_prob

    def test(self, test_data):
        start = time()
        total = 0.0
        errors = 0.0
        for root, dirs, files in os.walk(test_data, topdown=True):
            for name in files:
                if root.startswith('.') or name.startswith('.'):
                    continue 
                category = root.split('/')[-1]
                text = open(os.path.join(root, name), 'r').read().decode('utf-8')
                predict = self.predict(text)                
                total += 1
                if category != predict:
                    errors += 1
                    print 'predict: %s, actual: %s, errors percentage: %0.2f' % (predict.encode('utf-8'), category.encode('utf-8'), 100 * errors / total)
        print 'testing completed, total: %d, errors: %d, error rate:%0.2f, costs: %0.2f' % (total, errors, 100 * errors / total, time() - start)
        return errors / total

if __name__ == '__main__':    
    STOP_WORDS = set(line.strip().decode('utf-8') for line in open("stopwords.dic", 'r'))
    def tokenize(text):
        try:
            seg_list = jieba.cut(text, cut_all=False)
            zh_vocabulaly = re.compile(ur"([\u4E00-\u9FA5]+$)")            
            return set([x.strip() for x in seg_list if x not in STOP_WORDS])
        except Exception, e:
            print e
            return []        
    classifier = NaiveBayesClassifier(tokenizer=tokenize)
    classifier.fit(u'train_data/')
    classifier.dump('classifier.dat')
    # classifier.load(u'classifier.dat')    
    classifier.reduce(max_size=400, weighter=InformationGain)
    # for x in classifier.reduced_features.keys():
    #     print x.encode('utf-8')
    classifier.test(u'data_test1/')   
    