from bin.data_preparer import DataPreparer
from bin.price_guesser import PriceGuesser


class Main:
    if __name__ == "__main__":
        # data_preparer = DataPreparer()
        # data_preparer.prepare(sheet_name='Transakcje', path='/home/michal/repo/price-guesser/test-data/antyki.xls')

        price_guesser = PriceGuesser()
        # price_guesser.prepare_data(path='/home/michal/repo/price-guesser/test-data/antyki.xls')
        # price_guesser.describe_data(path='/home/michal/repo/price-guesser/test-data/antyki.xls')
        price_guesser.train(sheet_name='Transakcje', path='/home/michal/repo/price-guesser/test-data/antyki.xls')
