
import random

import profileapp


def generateRefPromo():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 6
    while True:
        promo = ''
        for i in range(length):
            promo += random.choice(chars)
        promos = profileapp.models.ReferralPromo.objects.filter(user_link=promo).first()
        if promos is None:
            break
    return promo
