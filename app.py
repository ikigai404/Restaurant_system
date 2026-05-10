from flask import Flask, render_template, request, make_response
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io

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
    
    """print(selected_items)
    print("HEREEEEEEEE")"""
    
     
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

@app.route('/download_invoice', methods=['POST'])
def download_invoice():
    # Get the order details sent from the ebill page
    order_number = request.form.get('order_number')
    date = request.form.get('date')
    items_raw = request.form.getlist('items')

    items = []
    total_price = 0
    for item_str in items_raw:
        name, price, quantity, total = item_str.split('|')
        price = float(price)
        quantity = int(quantity)
        total = float(total)
        items.append({'name': name, 'price': price, 'quantity': quantity, 'total': total})
        total_price += total

    # Create a PDF file in memory using ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, height - 55, "INVOICE")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, "Restaurant Management System")
    p.drawString(50, height - 100, f"E-Bill No: {order_number}")
    p.drawString(50, height - 120, f"Date: {date}")

    p.setFont("Helvetica-Bold", 11)
    y = height - 160
    p.drawString(50, y, "Item")
    p.drawString(270, y, "Price (Rs)")
    p.drawString(370, y, "Qty")
    p.drawString(450, y, "Total (Rs)")
    p.line(50, y - 8, 550, y - 8)

    p.setFont("Helvetica", 11)
    y -= 28
    for item in items:
        p.drawString(50, y, item['name'])
        p.drawString(270, y, f"{item['price']:.2f}")
        p.drawString(370, y, str(item['quantity']))
        p.drawString(450, y, f"{item['total']:.2f}")
        y -= 22

    p.line(50, y - 5, 550, y - 5)
    p.setFont("Helvetica-Bold", 13)
    p.setFillColor(colors.red)
    p.drawString(50, y - 25, f"Total Price: Rs {total_price:.2f}")

    p.setFillColor(colors.black)
    p.setFont("Helvetica", 9)
    p.drawString(50, 40, "© 2026 Restaurant Order System. All rights reserved.")

    p.showPage()
    p.save()

    # Send the PDF to the browser as a download
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=invoice_{order_number}.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
