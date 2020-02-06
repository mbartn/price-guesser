import pandas as pd

df = pd.read_excel('test-data/antyki.xls', 'Transakcje')
df = df.drop({'Lp', 'Data', 'Godzina', 'ID Sprzedawcy', 'Sprzedawca',
              'Miasto', 'Kod EAN', 'Do wyczer. zapas.',
              'Wartość', 'Kupujący', 'Kategoria 1'
              }, axis=1)
print('columns after drop:')
for el in df.head():
    print(el, end=' ')

df = df.rename(columns={"ID Aukcji (link)": "id", 'Aukcja': 'title', 'Rodzaj aukcji (KT/lic.)': 'auction_type',
                        'Stan': 'is_new', 'Sklep': 'is_shop', 'Strefa Marek': 'mark_zone',
                        'Wyróżnienie': 'wyroznienie_promotion',
                        'Str.działu': 'str_dzialu_promotion', 'Pogrubienie': 'pogrubienie_promotion',
                        'Podświetl.': 'podswietlenie_promotion', 'Cena': 'price', 'Ilość': 'amount',
                        })

print('columns after rename:')
for el in df.head():
    print(el, end=' | ')
