from flask import Flask, render_template, request
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # Renders index.html from the templates folder
    return render_template('index.html')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    # Renders place_order.html from the templates folder
    return render_template('place_order.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    category = request.args.get('category') 
    

    menu_items = [
        {"name": "Rice and Curry", "price": 300, "category": "sri_lankan"},
        {"name": "String Hoppers", "price": 300, "category": "sri_lankan"},
        {"name": "Hoppers", "price": 200, "category": "sri_lankan"},
        {"name": "Spaghetti", "price": 400, "category": "italian"},
        {"name": "Lasagna", "price": 500, "category": "italian"},
        {"name": "Pizza", "price": 600, "category": "italian"},
        {"name": "Fried Rice", "price": 350, "category": "chinese"},
        {"name": "Noodles", "price": 300, "category": "chinese"},
        {"name": "Chow Mein", "price": 400, "category": "chinese"},
        {"name": "Chicken Curry", "price": 350, "category": "indian"},
        {"name": "Pad Thai", "price": 450, "category": "thai"},
        {"name": "Tom Yum Goong", "price": 550, "category": "thai"},
        {"name": "Green Curry", "price": 400, "category": "thai"}

    ]
    
    beverages = [
        {"name": "Coke", "price": 100, "category": "beverages"},
        {"name": "Pepsi", "price": 100, "category": "beverages"},
        {"name": "Lemonade", "price": 150, "category": "beverages"},
        {"name": "Iced Tea", "price": 150, "category": "beverages"},
        {"name": "Coffee", "price": 200, "category": "beverages"},
        {"name": "Tea", "price": 150, "category": "beverages"}
    ]

    if category != 'all':
        items = [item for item in menu_items if item['category'] == category]
    else:
        items = menu_items

    # Renders menu.html from the templates folder
    return render_template('menu.html', items= items, selected_category=category if not category == 'all' else None, beverages= beverages)

@app.route('/review_order', methods=['GET', 'POST'])
def order_summary():
    # Implementation for order summary page
    selected_items = request.form.getlist('selected_items')
    
    order_details = []
    total_price = 0
    
    for item in selected_items:
        name, price = item.split('|', 1)
        price = int(price)
        quantity = int(request.form.get(f'quantity_{name}', 1))
        item_total = price * quantity
        
        order_details.append({'name': name, 'price': price, 'quantity': quantity, 'total': item_total})
        total_price += item_total
    
    return render_template('review_order.html', selected_items=order_details, total_price=total_price)

@app.route('/ebill', methods=['GET', 'POST'])
def ebill():    
    # Renders ebill.html from the templates folder
    selected_items = request.form.getlist('items')
    
    print(selected_items)
    print("HEREEEEEEEE")
    
     
    order_details = []
    total_price = 0   
    
    for item in selected_items:

        name, price, quantity = item.split('|', 2)
        price = int(price)
        quantity = int(quantity)
        item_total = price * quantity
        
        order_details.append({'name': name, 'price': price, 'quantity': quantity, 'total': item_total})
        total_price += item_total

    return render_template('ebill.html', order_details=order_details, total_price=total_price, order_number=random.randint(1000, 9999), date=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

if __name__ == '__main__':
    app.run(debug=True)