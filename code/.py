import cs50
def main():
    c = cs50.get_int('Card Number: ')
    n = len(str(c))
    if n not in (13,15,16):
        print('INVALID')
    sum = 0
    for i in range(n + 1):
        digit = c % 10
        if i % 2 != 0:
            digit = digit * 2
            if digit > 9:
                digit -= 9
        sum += digit
        c = int(c / 10)
    
    while c > 100:
        c = int(c / 10)
    
    if not sum % 10 == 0:
        print('INVALID')
    elif c > 50 and c < 56 and n == 16:
        print('MASTERCARD')
    elif c in (34,37) and n == 15:
        print('AMEX')
    elif int(c / 10) == 4 and n in (13, 16):
        print('VISA')
    else:
        print('INVALID')