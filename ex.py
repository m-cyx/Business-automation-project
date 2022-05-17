while True:
    s = input('Введите число ')  # получаем строку
    try:
        n = int(s)  # пробуем перевести в число, если не удается переходим в except
        print("окей")
        break
        
    except:
        if s.isalpha():  # функция isalpha возвращает True если все символы буквы
            print("Введены буквы")
        else:
            print("Введены непонятные символа")

print('пошло дальше')