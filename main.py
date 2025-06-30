import csv
import sys
from tabulate import tabulate

# Функция для загруски CSV файла, возвращает список
def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def filter_data(data, column, operator, value):
    filtered = []
    for row in data:
        if column not in row:
            continue
        cell = row[column]

        if is_number(cell) and is_number(value):
            cell_val = float(cell)
            value_val = float(value)
            if operator == '>' and cell_val > value_val:
                filtered.append(row)
            elif operator == '<' and cell_val < value_val:
                filtered.append(row)
            elif operator == '=' and cell_val == value_val:
                filtered.append(row)
        else:
            if operator == '=' and str(cell).strip().lower() == value.strip().lower():
                filtered.append(row)
    return filtered

def aggregate(data, column, operation):
    values = []
    for row in data:
        try:
            values.append(float(row[column]))
        except (ValueError, KeyError):
            continue

    if not values:
        return None

    if operation == 'avg':
        return round(sum(values) / len(values), 2)
    elif operation == 'min':
        return min(values)
    elif operation == 'max':
        return max(values)

def main():

    # Создаем переменную аргументы и записываем в нее все переданные аргументы по порядку
    arguments = sys.argv


    # Далее проверяем аргументы на то, если передали всего две пазиции, значит выводим весь список из CSV файла
    if len(arguments) == 2:
        file_path = arguments[1]
        data = load_csv(file_path)
        if data:
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("Данный файл пуст или не читается")
        return


    # Также проверяем количество аргументов, если меньше шести, выходим из программы и сигнализируем об ошибки
    if len(arguments) < 6:
        sys.exit(1)


    # Распределяем все полученные аргументы по переменным
    file_path = arguments[1]
    filter_column = arguments[2]
    operator = arguments[3]
    filter_value = arguments[4]
    agg_column = arguments[5]
    operation = arguments[6] if len(arguments) > 6 else 'avg'


    # Получаем данные из переданного файла и записываем их в переменную data
    data = load_csv(file_path)

    # Создаем список отфильтрованных данных
    filtered = filter_data(data, filter_column, operator, filter_value)

    # Вывод отфильтрованных строк в виде таблицы используя библиотеку "tabulate"
    if filtered:
        print(tabulate(filtered, headers="keys", tablefmt="grid"))
    else:
        print("Нет данных, удовлетворяющих условиям фильтрации.")

    # Агрегация
    result = aggregate(filtered, agg_column, operation)
    print(f"\n Агрегация '{operation}' по полю '{agg_column}': {result}")

if __name__ == "__main__":
    main()


# Список нескольких команд для терминала

# python main.py products.csv brand "=" apple price avg
# python main.py products.csv price "<" 1000 rating max
# python main.py products.csv