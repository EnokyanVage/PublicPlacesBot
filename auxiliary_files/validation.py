import re

valid_patternName = re.compile(r"^[а-яА-ЯёЁa-zA-Z]+$", re.I)
valid_patternAge = re.compile(r"^[z0-9]+$", re.I)
valid_patternPhone = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{10,10}$", re.I)
valid_patternText = re.compile(r"^[а-яА-ЯёЁa-zA-Z0-9-.,/! ]+$", re.I)
valid_patternGeo = re.compile(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", re.I)

list_city = {'Новосибирск': 1}

def validateName(name: str) -> bool:
    return bool(valid_patternName.match(name))
    
def validateSurname(surname: str) -> bool:
   return bool(valid_patternName.match(surname))   
   
def validateAge(age: str) -> bool:
   return bool(valid_patternAge.match(age))

def validatePhone(phone: str) -> bool:
   return bool(valid_patternPhone.match(phone))

def validationText(text: str) -> bool:
    return True#bool(valid_patternText.match(text))

def validationGeo(geo: str) ->bool:
    return bool(valid_patternGeo.match(geo))

def years(age):
    if(age%10 == 1 and age%100 != 11):
        return str(age) + " Год"
    elif(1 < age % 10 <= 4 and age%100!=12 and age%100!=13 and age%100!=14):
        return str(age) + " Года"
    else:
        return str(age) + " Лет"

def pps(pp):
    if(pp%10 == 1 and pp%100 != 11):
        return str(pp) + " общественное место"
    elif(1 < pp % 10 <= 4 and pp%100!=12 and pp%100!=13 and pp%100!=14):
        return str(pp) + " общественных мест"
    else:
        return str(pp) + " общественных мест"
        
def check_city(city):
    if city not in list_city.keys():
        return False
    return True
    
