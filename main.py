import os
import matplotlib.pyplot as plt

file_name = "data.txt" #указываем имя файла
absolut_path = os.path.abspath(file_name) #абсолютный путь до файла

sales_list = []#список продаж
total_sales = {}#общая стоимость продаж каждого продукта
total_sales_by_date = {}#общая стоимость продаж по датам

product_highest_revenue = None #Продукт который принёс наибольшую выручу
day_highest_revenue = None #День с наибольшей суммой продаж

#возвращает список продаж
def read_sales_data(file_path):
    items_labels = ["product_name", "quantity", "price", "date"]#наименование свойств

    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            for i in range(len(lines)):
                item = {}
                for j in range(len(lines[i].split(", "))):
                    text = lines[i].split(", ")[j]
                    digit = text.isdigit()
                    if digit:
                        item[items_labels[j]] = int(lines[i].split(", ")[j])
                    else:
                        item[items_labels[j]] = lines[i].split(", ")[j]
                sales_list.append(item)
            return sales_list
    except Exception as e:
        print(f"Не удалось открыть файл: {e}")
    finally:
        print("Файл успешно прочитан: список продаж сформирован!")

read_sales_data(absolut_path)

#возвращает словарь общая сумма для каждого продукта
def total_sales_per_product(sales_data): 
    for i in range(len(sales_data)):
        item = sales_data[i]
        total_sale = item["quantity"] * item["price"]

        if item["product_name"] in total_sales:
            continue

        for j in range(i + 1, len(sales_data)):
            item_j = sales_data[j]
            if item["product_name"] == item_j["product_name"]:
                total_sale_j = item_j["quantity"] * item_j["price"]
                total_sale += total_sale_j
        total_sales[item["product_name"]] = total_sale
    return total_sales

total_sales_per_product(sales_list)

#возвращает словарь общая сумма для каждой даты
def sales_over_time(sales_data): 
    for i in range(len(sales_data)):
        item = sales_data[i]
        total_sale = item["quantity"] * item["price"]

        if item["date"] in total_sales_by_date:
            continue

        for j in range(i + 1, len(sales_data)):
            item_j = sales_data[j]
            if item["date"] == item_j["date"]:
                total_sale_j = item_j["quantity"] * item_j["price"]
                total_sale += total_sale_j
        total_sales_by_date[item["date"]] = total_sale
    return total_sales_by_date

sales_over_time(sales_list)

product_highest_revenue = max(total_sales, key=total_sales.get)
day_highest_revenue = max(total_sales_by_date, key=total_sales_by_date.get)

print(f"Продукт который принес наибольшую выручку: {product_highest_revenue}")
print(f"День который принес наибольшую выручку: {day_highest_revenue}")

#графики
fig, axes = plt.subplots(1, 2, figsize=(15,5))

#график общей суммы продаж по каждому продукту.
products = list(total_sales.keys())
products_values = list(total_sales.values())

axes[0].bar(products, products_values, color='blue')
axes[0].set_xlabel('Продукты')
axes[0].set_ylabel('Общая сумма продаж')
axes[0].set_title('График №1: Общая сумма продаж по продуктам')
axes[0].set_xticks(range(len(products)))
axes[0].set_xticklabels(products, rotation=45, ha='right')
axes[0].grid(axis='y')

#график общей суммы продаж по дням.
days = list(total_sales_by_date.keys())
days_value = list(total_sales_by_date.values())

axes[1].bar(days, days_value, color='green')
axes[1].set_xlabel('Дни')
axes[1].set_ylabel('Общая сумма продаж')
axes[1].set_title('График №2: Общая сумма продаж по дням')
axes[1].set_xticks(range(len(days)))
axes[1].set_xticklabels(days, rotation=45, ha='right')
axes[1].grid(axis='y')

#рисуем наши графики
plt.tight_layout()
plt.show()




