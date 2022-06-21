from datetime import datetime
from math import ceil



def get_tour_discounted_price(obj):
    if obj.price and obj.discount and obj.discount_starts and  obj.discount_finish and obj.discount_starts < datetime.today().date() and  obj.discount_finish > datetime.today().date():
        return round(obj.price - obj.price*(obj.discount/100)) if obj.discount_in_prc else obj.price - obj.discount
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