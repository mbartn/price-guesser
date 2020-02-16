import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer


class PriceGuesser:

    def prepare_data(self):
        df = pd.read_excel('test-data/antyki.xls', 'Transakcje')
        df = df.drop({'Lp', 'Data', 'Godzina', 'ID Sprzedawcy', 'Sprzedawca',
                      'Miasto', 'Kod EAN', 'Do wyczer. zapas.',
                      'Wartość', 'Kupujący', 'Kategoria 1'
                      }, axis=1)
        print('columns after drop:')
        print(df.columns)

        df = df.rename(columns={"ID Aukcji (link)": "id", 'Aukcja': 'title', 'Rodzaj aukcji (KT/lic.)': 'auction_type',
                                'Stan': 'is_new', 'Sklep': 'is_shop', 'Strefa Marek': 'mark_zone',
                                'Wyróżnienie': 'wyroznienie_promotion',
                                'Str.działu': 'str_dzialu_promotion', 'Pogrubienie': 'pogrubienie_promotion',
                                'Podświetl.': 'podswietlenie_promotion', 'Cena': 'price', 'Ilość': 'amount',
                                })

        print('columns after rename:')
        print(df.columns)

        df.loc[df.is_new != 'nowy', 'is_new'] = 0
        df.loc[df.is_new == 'nowy', 'is_new'] = 1

        self.merge_categories(df=df)

        df = df.drop({'Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                      'Kategoria 8'
                      }, axis=1)
        writer_orig = pd.ExcelWriter('test-data/antyki-prepared-data.xls')
        df.to_excel(writer_orig, index=False, sheet_name='antyki')
        writer_orig.save()

    def describeData(self):
        df = pd.read_excel('test-data/antyki-prepared-data.xls', 'antyki')
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
        df = pd.read_excel('test-data/antyki-prepared-data.xls', 'antyki')
        print(df.columns)
        to_categorical(df)
        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]
        test_new = test.drop('price', axis=1)
        y_test = np.log1p(test["price"])

        nrow_train = train.shape[0]
        y = np.log1p(train["price"])
        merge: pd.DataFrame = pd.concat([train, test_new])

        cv = CountVectorizer(min_df=10)
        X_name = cv.fit_transform(merge['title'])
        cv = CountVectorizer()
        X_category = cv.fit_transform(merge['category'])



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


@staticmethod
def merge_categories(df):
    df['category'] = df.loc[:,
                     ['Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                      'Kategoria 8']].apply(
        lambda x: '-'.join(x.dropna().astype(str)), axis=1

    )
