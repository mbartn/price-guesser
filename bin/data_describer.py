import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class DataDescriber:
    @staticmethod
    def describe_data(self, path: str, sheet_name: str):
        df = pd.read_excel(path, sheet_name)

        print(df.price.describe())
        print(df.title.describe())
        print(df.category.describe())

        print('There are',
              df['category'].nunique(),
              'unique values in category name column')

        print(df['category'].value_counts()[:10])
        sns.boxplot(x='is_new', y=np.log(df['price'] + 1), data=df,
                    palette=sns.color_palette('RdBu', 5))

        plt.subplot(1, 2, 1)
        (df['price']).plot.hist(bins=50, figsize=(12, 6), edgecolor='white', range=[0, 250])
        plt.xlabel('price', fontsize=12)
        plt.title('Price Distribution', fontsize=12)
        plt.show()

        plt.subplot(1, 2, 2)
        np.log(df['price'] + 1).plot.hist(bins=50, figsize=(12, 6), edgecolor='white')
        plt.xlabel('log(price+1)', fontsize=12)
        plt.title('Price Distribution', fontsize=12)
        plt.show()

        price_from_users = df.loc[df['is_shop'] == 'N', 'price']
        price_from_shops = df.loc[df['is_shop'] == 'T', 'price']

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
