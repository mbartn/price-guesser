import os

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_squared_error


class PriceGuesser:
    cv = CountVectorizer(dtype=np.float64)

    @staticmethod
    def train(sheet_name: str, path: str):
        df = pd.read_excel(path, sheet_name)
        df = df.drop({'id', 'auction_type', 'is_new',
                      'is_shop', 'mark_zone', 'wyroznienie_promotion', 'str_dzialu_promotion', 'pogrubienie_promotion',
                      'podswietlenie_promotion', 'amount', 'category'}, axis=1)
        print('columns after drop:')
        print(df.columns)

        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]
        test_new = test.drop('price', axis=1)
        y_test = np.log1p(test["price"])

        nrow_train = train.shape[0]
        y = np.log1p(train["price"])
        merge: pd.DataFrame = pd.concat([train, test_new], sort=True)

        x_title = PriceGuesser.cv.fit_transform(merge['title'])

        x_title_csr = x_title.tocsr()

        mask = np.array(np.clip(x_title_csr.getnnz(axis=0) - 1, 0, 1), dtype=bool)
        x_title_csr = x_title_csr[:, mask]
        x = x_title_csr[:nrow_train]
        x_test = x_title_csr[nrow_train:]
        train_x = lgb.Dataset(x, label=y)

        params = {
            'learning_rate': 0.75,
            'application': 'regression',
            'max_depth': 3,
            'num_leaves': 100,
            'verbosity': -1,
            'metric': 'RMSE',
        }
        gbm = lgb.train(params, train_set=train_x, num_boost_round=3200, verbose_eval=100)

        y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration)
        print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        gbm.save_model(dir_path + '/../model/model.txt')

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
