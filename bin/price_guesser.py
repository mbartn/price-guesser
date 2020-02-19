import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_squared_error




class PriceGuesser:


    def describe_data(self, path: str):
        df = pd.read_excel(path, 'antyki')
        print(df.columns)
        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]

        print(train.price.describe())
        print(train.title.describe())
        print(train.category.describe())

        print('There are',
              train['category'].nunique(),
              'unique values in category name column')
        print(train['category'].value_counts()[:10])

        sns.boxplot(x='is_new', y=np.log(train['price'] + 1), data=train,
                    palette=sns.color_palette('RdBu', 5))

        plt.subplot(1, 2, 1)
        (train['price']).plot.hist(bins=50, figsize=(12, 6), edgecolor='white', range=[0, 250])
        plt.xlabel('price', fontsize=12)
        plt.title('Price Distribution', fontsize=12)
        plt.show()

        plt.subplot(1, 2, 2)
        np.log(train['price'] + 1).plot.hist(bins=50, figsize=(12, 6), edgecolor='white')
        plt.xlabel('log(price+1)', fontsize=12)
        plt.title('Price Distribution', fontsize=12)
        plt.show()

        price_from_users = train.loc[df['is_shop'] == 'N', 'price']
        price_from_shops = train.loc[df['is_shop'] == 'T', 'price']

        fig, ax = plt.subplots(figsize=(18, 8))
        ax.hist(np.log(price_from_shops + 1), color='#007D00', alpha=1.0, bins=50, range=[0, 10],
                label='Price from shops')
        ax.hist(np.log(price_from_users + 1), color='#8CB4E1', alpha=0.7, bins=50, range=[0, 10],
                label='Price from users')
        plt.xlabel('price', fontsize=12)
        plt.ylabel('frequency', fontsize=12)
        plt.title('Price Distribution by Shipping Type', fontsize=15)
        plt.tick_params(labelsize=12)
        plt.legend()
        plt.show()

        print('The average price is {}'.format(round(price_from_users.mean(), 2)), 'from users');
        print('The average price is {}'.format(round(price_from_shops.mean(), 2)), 'from sellers')

    def train(self):
        df = pd.read_excel('/home/michal/repo/price-guesser/test-data/antyki-prepared-data.xls', 'antyki')
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
        merge: pd.DataFrame = pd.concat([train, test_new])

        NAME_MIN_DF = 10
        cv = CountVectorizer(min_df=NAME_MIN_DF, dtype=np.float64)
        x_title = cv.fit_transform(merge['title'])

        # x_title_csr = hstack((x_title)).tocsr()
        x_title_csr = x_title.tocsr()
        print()

        mask = np.array(np.clip(x_title_csr.getnnz(axis=0) - 1, 0, 1), dtype=bool)
        x_title_csr = x_title_csr[:, mask]
        X = x_title_csr[:nrow_train]
        X_test = x_title_csr[nrow_train:]

        train_X = lgb.Dataset(X, label=y)

        params = {
            'learning_rate': 0.75,
            'application': 'regression',
            'max_depth': 3,
            'num_leaves': 100,
            'verbosity': -1,
            'metric': 'RMSE',
        }
        gbm = lgb.train(params, train_set=train_X, num_boost_round=3200, verbose_eval=100)

        y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
        print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)




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
