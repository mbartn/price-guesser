import numpy as np
import pandas as pd


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

        print(df.head(10))
        print(df.columns)

        writer_orig = pd.ExcelWriter('C:\\Users\\micha\\Desktop\\formatted.xls')
        df.to_excel(writer_orig, index=False, sheet_name='report')
        writer_orig.save()

        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]

        print(train.head())
        print(train.info())

    @staticmethod
    def merge_categories(df):
        df['category'] = df.loc[:,
                         ['Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                          'Kategoria 8']].apply(
            lambda x: '-'.join(x.dropna().astype(str)), axis=1

        )
