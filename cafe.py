import json
from datetime import date

FILE_NAME = "orders.json"

MENU = {
    1: {"name": "Капучино", "price": 65},
    2: {"name": "Американо", "price": 55},
    3: {"name": "Чізкейк", "price": 90},
    4: {"name": "Круасан", "price": 60},
    5: {"name": "Лате", "price": 70},
}


def load_orders():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            orders = json.load(file)
    except FileNotFoundError:
        return [], 1

    if not isinstance(orders, list):
        raise ValueError(f"Файл {FILE_NAME} має містити список замовлень.")

    order_id = max((order["id"] for order in orders), default=0) + 1
    return orders, order_id


def save_orders(orders):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)


def show_menu_items():
    print("\n--- Меню кафе ---")
    for number, item in MENU.items():
        print(f"{number}. {item['name']} — {item['price']} грн")


def show_menu():
    print("\n--- Кафе: консольне меню ---")
    print("1. Створити замовлення")
    print("2. Переглянути всі замовлення")
    print("3. Видалити замовлення")
    print("4. Знайти замовлення за датою")
    print("5. Вийти")


def create_order(orders, order_id):
    while True:
        try:
            table = int(input("Введіть номер столика: "))
            break
        except ValueError:
            print("Введіть ціле число.")

    items = []
    show_menu_items()
    while True:
        try:
            number = int(input("Введіть номер страви (0 — завершити вибір): "))
        except ValueError:
            print("Введіть ціле число.")
            continue

        if number == 0:
            break
        if number not in MENU:
            print("Такої страви немає в меню.")
            continue

        while True:
            try:
                qty = int(input("Введіть кількість: "))
                if qty <= 0:
                    print("Кількість має бути більшою за нуль.")
                    continue
                break
            except ValueError:
                print("Введіть ціле число.")

        menu_item = MENU[number]
        items.append({
            "name": menu_item["name"],
            "price": menu_item["price"],
            "qty": qty,
        })

    total = sum(item["price"] * item["qty"] for item in items)
    order = {
        "id": order_id,
        "table": table,
        "items": items,
        "total": total,
        "date": date.today().isoformat(),
        "status": "нове",
    }
    orders.append(order)
    save_orders(orders)
    print(f"Замовлення №{order_id} створено. Сума: {total} грн.")
    return order_id + 1


def show_orders(orders):
    if not orders:
        print("Замовлень немає.")
        return

    for order in orders:
        print(
            f"\nЗамовлення №{order['id']} | Столик: {order['table']} | "
            f"Дата: {order['date']} | Статус: {order['status']}"
        )
        for item in order["items"]:
            print(
                f"  {item['name']} — {item['qty']} шт. "
                f"× {item['price']} грн"
            )
        print(f"Сума: {order['total']} грн")


def delete_order(orders):
    try:
        order_id = int(input("Введіть ID замовлення для видалення: "))
    except ValueError:
        print("ID має бути цілим числом.")
        return

    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            save_orders(orders)
            print(f"Замовлення №{order_id} видалено.")
            return

    print(f"Замовлення з ID {order_id} не знайдено.")


def find_by_date(orders):
    order_date = input("Введіть дату (РРРР-ММ-ДД): ")
    matching_orders = [
        order for order in orders if order["date"] == order_date
    ]
    if not matching_orders:
        print("Замовлень за цією датою не знайдено.")
        return

    show_orders(matching_orders)


def main():
    orders, order_id = load_orders()
    while True:
        show_menu()
        choice = input("Оберіть дію: ")
        if choice == "1":
            order_id = create_order(orders, order_id)
        elif choice == "2":
            show_orders(orders)
        elif choice == "3":
            delete_order(orders)
        elif choice == "4":
            find_by_date(orders)
        elif choice == "5":
            print("До побачення!")
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
