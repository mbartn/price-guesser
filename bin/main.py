import os

from bin.price_guesser import PriceGuesser


class Main:
    if __name__ == "__main__":
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # data_preparer = DataPreparer()
        # data_preparer.prepare(sheet_name='Transakcje', path='/home/michal/repo/price-guesser/test-data/antyki.xls')

        price_guesser = PriceGuesser()
        # price_guesser.prepare_data(path='/home/michal/repo/price-guesser/test-data/antyki.xls')
        # price_guesser.describe_data(path='/home/michal/repo/price-guesser/test-data/antyki.xls')
        # price_guesser.train(sheet_name='antyki', path=dir_path + '/../test-data/antyki-prepared-data.xls')
        price_guesser.guess_price('1990 rower z prl')
