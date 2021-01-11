import numpy as np
import os
import pandas as pd
from pandas import DataFrame


class DataPreparer:
    @staticmethod
    def prepare(path: str, sheet_name: str):
        data_frame = pd.read_excel(path, sheet_name)

        print('Dropping unnecessary columns...')
            data_frame = data_frame.drop({'Lp', 'Data', 'Godzina', 'ID Sprzedawcy', 'Sprzedawca',
                                          'Miasto', 'Kod EAN', 'Do wyczer. zapas.',
                                          'Wartość', 'Kupujący', 'Kategoria 1'
                                      }, axis=1)
        print('columns left: ')
        print(data_frame.columns)

        print('Renaming columns...')
        data_frame = data_frame.rename(
            columns={"ID Aukcji (link)": "id", 'Aukcja': 'title', 'Rodzaj aukcji (KT/lic.)': 'auction_type',
                     'Stan': 'is_new', 'Sklep': 'is_shop', 'Strefa Marek': 'mark_zone',
                     'Wyróżnienie': 'wyroznienie_promotion',
                     'Str.działu': 'str_dzialu_promotion', 'Pogrubienie': 'pogrubienie_promotion',
                     'Podświetl.': 'podswietlenie_promotion', 'Cena': 'price', 'Ilość': 'amount',
                     })
        print('columns after rename:')
        print(data_frame.columns)

        data_frame.loc[data_frame.is_new != 'nowy', 'is_new'] = 0
        data_frame.loc[data_frame.is_new == 'nowy', 'is_new'] = 1

        data_frame = DataPreparer.__merge_categories(df=data_frame)

        msk = np.random.rand(len(data_frame)) < 0.8
        train = data_frame[msk]
        test = data_frame[~msk]

        dir_path = os.path.dirname(os.path.realpath(__file__))
        DataPreparer.__save_to_file(path=dir_path + '/../test-data/antyki-prepared-full.xls', df=train,
                                    sheet_name=sheet_name)
        # DataPreparer.__save_to_file(path=dir_path + '/../test-data/antyki-train.xls', df=train,
        #                             sheet_name=sheet_name)
        # DataPreparer.__save_to_file(path=dir_path + os.pardir + '/../test-data/antyki-test.xls', df=test,
        #                             sheet_name=sheet_name)

    @staticmethod
    def __merge_categories(df: DataFrame):
        df['category'] = df.loc[:,
                         ['Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                          'Kategoria 8']].apply(
            lambda x: '-'.join(x.dropna().astype(str)), axis=1
        )
        df = df.drop(
            {'Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
             'Kategoria 8'
             }, axis=1)
        return df

    @staticmethod
    def __save_to_file(df: DataFrame, path: str, sheet_name: str):
        writer_orig = pd.ExcelWriter(path)
        df.to_excel(writer_orig, index=False, sheet_name=sheet_name)
        writer_orig.save()
