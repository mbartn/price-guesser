import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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

    @staticmethod
    def merge_categories(df):
        df['category'] = df.loc[:,
                         ['Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                          'Kategoria 8']].apply(
            lambda x: '-'.join(x.dropna().astype(str)), axis=1

        )
