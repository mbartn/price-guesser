import os

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import mean_squared_error


class PriceGuesser:
    cv = CountVectorizer(dtype=np.float64)

    @staticmethod
    def train():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        df_train = pd.read_excel(dir_path + '/../test-data/antyki-train.xls', 'Transakcje')
        df_test = pd.read_excel(dir_path + '/../test-data/antyki-test.xls', 'Transakcje')
        df_train = df_train.drop({'id', 'is_new',
                                  'is_shop', 'mark_zone', 'wyroznienie_promotion', 'str_dzialu_promotion',
                                  'pogrubienie_promotion',
                                  'podswietlenie_promotion', 'amount', 'category'}, axis=1)  # todo: remove me
        df_test = df_test.drop({'id', 'is_new',
                                'is_shop', 'mark_zone', 'wyroznienie_promotion', 'str_dzialu_promotion',
                                'pogrubienie_promotion',
                                'podswietlenie_promotion', 'amount', 'category'}, axis=1)  # todo: remove me

        print('columns after drop:')
        print(df_train.columns)
        print(df_test.columns)

        y_train = df_train['price']
        y_test = df_test['price']

        x_train = df_train.drop('price', axis=1)
        x_test = df_test.drop('price', axis=1)

        y_test = np.log1p(y_test)
        y_train = np.log1p(y_train)

        tfidf_vec = TfidfVectorizer(dtype=np.float32, sublinear_tf=True, use_idf=True, smooth_idf=True)
        x_train_cv = tfidf_vec.fit_transform(x_train['title'])
        x_test_cv = tfidf_vec.fit_transform(x_test['title'])
        x_train['auction_type'] = x_train['auction_type'].astype('category')
        x_test['auction_type'] = x_test['auction_type'].astype('category')

        x_train['title'] = pd.DataFrame(x_train_cv.todense()).astype('float64')  # why todense()?
        x_test['title'] = pd.DataFrame(x_test_cv.todense()).astype('float64')

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

    # x_title_csr = x_title.tocsr()
    #
    # mask = np.array(np.clip(x_title_csr.getnnz(axis=0) - 1, 0, 1), dtype=bool)
    # x_title_csr = x_title_csr[:, mask]
    # x = x_title_csr[:nrow_train]
    # x_test = x_title_csr[nrow_train:]
    # train_x = lgb.Dataset(x, label=y)
    #

    # gbm = lgb.train(params, train_set=train_x, num_boost_round=3200, verbose_eval=100)
    #
    # y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration)
    # print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)
    #
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # gbm.save_model(dir_path + '/../model/model.txt')

    @staticmethod
    def guess_price(title: str):
        model = lgb.Booster(model_file=os.path.dirname(os.path.realpath(__file__)) + '/../model/model.txt')

        x_title = PriceGuesser.cv.fit_transform([title]).tocsr()
        y_pred = model.predict(x_title, num_iteration=model.best_iteration)
        print(y_pred)


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
