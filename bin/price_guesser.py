import os

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class PriceGuesser:
    cv = CountVectorizer(dtype=np.float64)

    @staticmethod
    def train():
        dir_path = os.path.dirname(os.path.realpath(__file__))

        df = pd.read_excel(dir_path + '/../test-data/antyki-prepared-full.xls', 'Transakcje')
        df = df.drop({'id', 'amount'}, axis=1)  # todo: remove me

        print('columns after drop:')
        print(df.columns)

        y = df['price']
        x = df.drop('price', axis=1)
        y = np.log1p(y)
        tfidf_vec = TfidfVectorizer(dtype=np.float32, sublinear_tf=True, use_idf=True, smooth_idf=True)
        x_cv = tfidf_vec.fit_transform(x['title'])
        x['title'] = pd.DataFrame(x_cv.todense()).astype('float64')  # why todense()?
        PriceGuesser.to_categorical(x)

        x_train, x_test = train_test_split(x, test_size=0.2)
        y_train, y_test = train_test_split(y, test_size=0.2)

        lgb_train = lgb.Dataset(x_train, y_train)
        lgb_eval = lgb.Dataset(x_test, y_test, reference=lgb_train)

        params = {
            'learning_rate': 0.75,
            'application': 'regression',
            'max_depth': 3,
            'num_leaves': 100,
            'verbosity': -1,
            'metric': 'RMSE',
        }

        print('training started')
        gbm = lgb.train(params,
                        lgb_train, num_boost_round=3200, verbose_eval=100)
        y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration)

        print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

    @staticmethod
    def guess_price(title: str):
        model = lgb.Booster(model_file=os.path.dirname(os.path.realpath(__file__)) + '/../model/model.txt')

        x_title = PriceGuesser.cv.fit_transform([title]).tocsr()
        y_pred = model.predict(x_title, num_iteration=model.best_iteration)
        print(y_pred)

    @staticmethod
    def to_categorical(dataset):
        dataset['auction_type'] = dataset['auction_type'].astype('category')
        dataset['is_new'] = dataset['is_new'].astype('category')
        dataset['is_shop'] = dataset['is_shop'].astype('category')
        dataset['mark_zone'] = dataset['mark_zone'].astype('category')
        dataset['wyroznienie_promotion'] = dataset['wyroznienie_promotion'].astype('category')
        dataset['str_dzialu_promotion'] = dataset['str_dzialu_promotion'].astype('category')
        dataset['pogrubienie_promotion'] = dataset['pogrubienie_promotion'].astype('category')
        dataset['podswietlenie_promotion'] = dataset['podswietlenie_promotion'].astype('category')
        dataset['category'] = dataset['category'].astype('category')
