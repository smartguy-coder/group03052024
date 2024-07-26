from gettext import translation

lang = 'en'

translator = translation('this_project', localedir='locale', languages=[lang], fallback=True)
_ = translator.gettext

welcome = _('Welcome')
print(welcome)

buy = _('Buy')
print(buy)

welcome2 = _('Welcome')
print(welcome2)

number = 77
sell = _('Sell {number} IPhones').format(number=77)
print(sell)
