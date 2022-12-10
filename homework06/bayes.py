from collections import defaultdict
from math import log
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.total = defaultdict(int)
        self.good = defaultdict(int)
        self.maybe = defaultdict(int)
        self.never = defaultdict(int)
        for i in range(len(X)):
            for word in clean(X[i]).split():
                word = word.lower().strip()
                self.total[word] += 1
                if y[i] == "good":
                    self.good[word] += 1
                elif y[i] == "maybe":
                    self.maybe[word] += 1
                elif y[i] == "never":
                    self.never[word] += 1

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        res = []
        for s in X:
            values = {"good": log(0.33), "maybe": log(0.33), "never": log(0.33)}
            for word in s.split():
                values["good"] += log((self.good[word] + self.alpha) / (
                    self.total[word] + self.alpha * len(self.total)))
                values["maybe"] += log((self.maybe[word] + self.alpha) / (
                    self.total[word] + self.alpha * len(self.total)))
                values["never"] += log((self.never[word] + self.alpha) / (
                    self.total[word] + self.alpha * len(self.total)))
            res.append(max(values, key=values.get))
        return res

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        accurate = 0
        predictions = self.predict(X_test)
        for i in range(len(X_test)):
            accurate += predictions[i] == y_test[i]
        return accurate / len(X_test)
