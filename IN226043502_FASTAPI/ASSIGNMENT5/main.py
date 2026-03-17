from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ══ MODELS ════════════════════════════════════════════════════════

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

class NewProduct(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    in_stock: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)

# ══ DATA ══════════════════════════════════════════════════════════

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
]

orders = []
order_counter = 1
cart = []

# ══ HELPERS ═══════════════════════════════════════════════════════

def find_product(product_id: int):
    return next((p for p in products if p['id'] == product_id), None)

def calculate_total(product: dict, quantity: int) -> int:
    return product['price'] * quantity

# ══ BASIC ENDPOINTS ═══════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ══ DAY 6 FEATURES (IMPORTANT) ════════════════════════════════════

# 🔍 SEARCH PRODUCTS
@app.get('/products/search')
def search_products(keyword: str = Query(...)):
    results = [p for p in products if keyword.lower() in p['name'].lower()]

    if not results:
        return {'message': f'No products found for: {keyword}'}

    return {
        'keyword': keyword,
        'total_found': len(results),
        'products': results
    }

# ↕ SORT PRODUCTS
@app.get('/products/sort')
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}

    reverse = (order == 'desc')
    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        'sort_by': sort_by,
        'order': order,
        'products': sorted_products
    }

# 📄 PAGINATION
@app.get('/products/page')
def paginate_products(page: int = 1, limit: int = 2):
    total = len(products)
    total_pages = -(-total // limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        'page': page,
        'limit': limit,
        'total_pages': total_pages,
        'products': products[start:end]
    }

# 🔍 SEARCH ORDERS
@app.get('/orders/search')
def search_orders(customer_name: str):
    results = [
        o for o in orders
        if customer_name.lower() in o['customer_name'].lower()
    ]

    if not results:
        return {'message': f'No orders found for: {customer_name}'}

    return {
        'customer_name': customer_name,
        'total_found': len(results),
        'orders': results
    }

# 📊 SORT BY CATEGORY + PRICE
@app.get('/products/sort-by-category')
def sort_by_category():
    sorted_products = sorted(
        products,
        key=lambda x: (x['category'], x['price'])
    )
    return sorted_products

# 🔥 SEARCH + SORT + PAGINATION (COMBINED)
@app.get('/products/browse')
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    # SORT
    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}

    reverse = (order == 'desc')
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    total_found = len(result)
    total_pages = -(-total_found // limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        'keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': page,
        'limit': limit,
        'total_found': total_found,
        'total_pages': total_pages,
        'products': result[start:end]
    }

# ⭐ BONUS — ORDERS PAGINATION
@app.get('/orders/page')
def paginate_orders(page: int = 1, limit: int = 3):
    total = len(orders)
    total_pages = -(-total // limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        'page': page,
        'limit': limit,
        'total_orders': total,
        'total_pages': total_pages,
        'orders': orders[start:end]
    }

# ══ CRUD + ORDERS + CART (UNCHANGED) ══════════════════════════════

@app.post('/products')
def add_product(new_product: NewProduct, response: Response):
    next_id = max(p['id'] for p in products) + 1
    product = {
        'id': next_id,
        'name': new_product.name,
        'price': new_product.price,
        'category': new_product.category,
        'in_stock': new_product.in_stock,
    }
    products.append(product)
    response.status_code = status.HTTP_201_CREATED
    return {'message': 'Product added', 'product': product}

@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter

    product = find_product(order_data.product_id)
    if not product:
        return {'error': 'Product not found'}

    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}

    order = {
        'order_id': order_counter,
        'customer_name': order_data.customer_name,
        'product': product['name'],
        'quantity': order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price': calculate_total(product, order_data.quantity),
        'status': 'confirmed',
    }

    orders.append(order)
    order_counter += 1

    return {'message': 'Order placed successfully', 'order': order}