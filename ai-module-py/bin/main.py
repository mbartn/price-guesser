import os

from bin.data_describer import DataDescriber
from bin.data_preparer import DataPreparer
from bin.price_guesser import PriceGuesser


class Main:
    if __name__ == "__main__":
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # DataDescriber.describe_data()

        # data_preparer = DataPreparer()
        # data_preparer.prepare(sheet_name='Transakcje', path=dir_path + '/../test-data/antyki.xls')

        price_guesser = PriceGuesser()
        # price_guesser.describe_data(path='/home/michal/repo/price-guesser/test-data/antyki.xls')
        #        price_guesser.train()
        price_guesser.guess_price('1990 rower z prl')

# data class AllegroAuction(
#     @BsonId
#     val id: Long, // id of the auction on Allegro
#     val title: String,
#     val auctionType: AuctionType,
#     val isNew: Boolean,
#     val price: String,
#     val alreadySold: Int,
#     val isCompany: Boolean,
#     val isMarkZone: Boolean, // Strefa marek
#     val isFeaturePromotion: Boolean, // Wyróżnienie
#     val isBoldPromotion: Boolean, // Pogrubienie
#     val isHighlightPromotion: Boolean // Podświetlenie
#     //val isStronaDzialuPromotion: Boolean, // these auctions are visible also on allegro.pl/promowane
# )
