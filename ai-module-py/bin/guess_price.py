import sys
from .price_guesser import PriceGuesser

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    id = sys.argv[1]
    title = sys.argv[2]
    auction_type = sys.argv[3]
    is_new = sys.argv[4]
    price = sys.argv[5]
    already_sold = sys.argv[6]
    is_company = sys.argv[7]
    is_mark_zone = sys.argv[8]
    is_feature_promotion = sys.argv[9]
    is_bold_promotion = sys.argv[10]
    is_highlight_promotion = sys.argv[11]
    is_strona_dzialu_promotion = sys.argv[12]

    print(f"Pytohon module is guessing price for auction: {id} {title}")
    price_guesser = PriceGuesser()

    price_guesser.guess_price()


