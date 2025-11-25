#!/usr/bin/env python3

print("🧮 Student Calculator v1.0 (Python)")
print("================================")

def calculator():
    while True:
        print("\nВыберите операцию:")
        print("1) Сложение")
        print("2) Вычитание")
        print("3) Умножение") 
        print("4) Деление")
        print("5) Выход")
        
        choice = input("Ваш выбор (1-5): ")
        
        if choice == '5':
            print("👋 До свидания!")
            break
            
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                
                if choice == '1':
                    result = num1 + num2
                    print(f"✅ Результат: {num1} + {num2} = {result}")
                elif choice == '2':
                    result = num1 - num2
                    print(f"✅ Результат: {num1} - {num2} = {result}")
                elif choice == '3':
                    result = num1 * num2
                    print(f"✅ Результат: {num1} * {num2} = {result}")
                elif choice == '4':
                    if num2 == 0:
                        print("❌ Ошибка: деление на ноль!")
                    else:
                        result = num1 / num2
                        print(f"✅ Результат: {num1} / {num2} = {result}")
            except ValueError:
                print("❌ Ошибка: введите числа!")
        else:
            print("❌ Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    calculator()
