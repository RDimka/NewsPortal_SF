from django import template

class CensorException(Exception):
   pass


register = template.Library()

#словарь
CENSORED_WORDS = [
   'spirit',
   'palit',
   'lovelace']

# Регистрируем наш фильтр под именем,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   try:
      if not isinstance(value, str):
         raise CensorException("Error: is not a text")

      for word in CENSORED_WORDS:
         if word in value:
            value = value.replace(word, word[:1]+"***")
         if word.capitalize() in value:
            value = value.replace(word.capitalize(), word.capitalize()[:1]+"***")
      # Возвращаемое функцией значение подставится в шаблон.
      return value
   except CensorException as e:
      print (e)