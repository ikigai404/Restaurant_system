from flask import Flask, render_template, request

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
        {"name": "rice and curry", "price": 300, "category": "sri_lankan"},
        {"name": "String Hoppers", "price": 300, "category": "sri_lankan"},
        {"name": "hoppers", "price": 200, "category": "sri_lankan"},
        {"name": "Spaghetti", "price": 400, "category": "italian"},
        {"name": "Lasagna", "price": 500, "category": "italian"},
        {"name": "pizza", "price": 600, "category": "italian"},
        {"name": "fried rice", "price": 350, "category": "chinese"},
        {"name": "noodles", "price": 300, "category": "chinese"},
        {"name": "chow mein", "price": 400, "category": "chinese"},
        {"name": "chicken curry", "price": 350, "category": "indian"},
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

    if category:
        menu_items = [item for item in menu_items if item['category'] == category]

    # Renders menu.html from the templates folder
    return render_template('menu.html', items=menu_items, selected_category=category, beverages=beverages)

@app.route('/review_order', methods=['GET', 'POST'])
def order_summary():
    # Implementation for order summary page
    selected_items = request.form.getlist('selected_items')
    
    order_details = []
    total_price = 0
    
    for item in selected_items:
        
        name, price = item.split('|')
        price = int(price)
        order_details.append({'name': name, 'price': price})
        total_price += price
    
    return render_template('review_order.html', selected_items=order_details, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
