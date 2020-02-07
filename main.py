import pandas as pd


def merge_categories():
    df['category'] = df.loc[:,
                     ['Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
                      'Kategoria 8']].apply(
        lambda x: '-'.join(x.dropna().astype(str)), axis=1

    )


# df = df.assign(
#     category=df['Kategoria 2'].dropna().astype(str) + '-' + df['Kategoria 3'].astype(str) + '-' + df['Kategoria 4'].astype(
#         str) + '-' + df['Kategoria 5'].astype(str) + '-' + df['Kategoria 6'].astype(str) + '-' + df[
#                  'Kategoria 7'].astype(
#         str) + '-' + df['Kategoria 8'].astype(str) + '-')


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

merge_categories()

df = df.drop({'Kategoria 2', 'Kategoria 3', 'Kategoria 4', 'Kategoria 5', 'Kategoria 6', 'Kategoria 7',
              'Kategoria 8'
              }, axis=1)

print(df.head(10))
print(df.columns)
