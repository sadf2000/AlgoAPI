def shift_text(mainText, olsdup, length, allSymbols="abcdefghijklmnopqrstuvwxyz0123456789"):
    mainText = mainText.lower()
    ciphertext = ""
    counter = 1
    counter2 = 1
    counter3 = 1
    
    for _ in range(len(mainText)):
        mainSymbol = mainText[counter2 - 1]  # -1 потому что в Python индексация с 0
        i = 0
        for _ in range(length):
            counter = 1
            while mainSymbol != allSymbols[counter - 1]:
                counter += 1
                if counter > len(allSymbols):
                    print("Ошибка: символ не найден")
                    return ""
            
            ciphertext += allSymbols[(counter + olsdup) % len(allSymbols) + i]
            counter3 += olsdup
            i += 1

        counter2 += 1
    
    return ciphertext

def unshift_text(ciphertext, olsdup, length, allSymbols="abcdefghijklmnopqrstuvwxyz0123456789"):

    L = len(allSymbols)
    plaintext = ""
    n = len(ciphertext)
    
    # Проверка кратности длины шифротекста длине блока
    if n % length != 0:
        print("Ошибка: длина шифротекста не кратна длине блока")
        return ""
    
    num_blocks = n // length
    
    for i in range(num_blocks):
        # Извлекаем первый символ текущего блока
        c0 = ciphertext[i * length]
        
        # Находим индекс первого символа в алфавите
        try:
            idx0 = allSymbols.index(c0)
        except ValueError:
            print(f"Ошибка: символ '{c0}' не найден в алфавите")
            return ""
        
        # Вычисляем позицию исходного символа
        p = (idx0 - olsdup - 1) % L
        plaintext += allSymbols[p]
    
    return plaintext
    
