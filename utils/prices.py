from datetime import datetime
from math import ceil



def get_tour_discounted_price(obj):
    if obj.price - obj.discounted_price:
        return obj.discounted_price
    else:
        return None


def get_tour_book_price(obj): 
    if obj.price:
        return ceil(obj.price*obj.prepay_amount/100) if obj.prepay_in_prc else obj.prepay_amount
    return None


def get_tour_daily_price(obj):
        discounted_price = get_tour_discounted_price(obj)
        if discounted_price:
            return round(discounted_price/obj.duration)
        if obj.price and obj.duration: 
            return round(obj.price/obj.duration)
        return None