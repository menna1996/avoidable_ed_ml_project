import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class Log1pTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return np.log1p(X)