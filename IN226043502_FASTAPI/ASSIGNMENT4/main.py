from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ---------------------------
# Sample Products Database
# ---------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

orders = []
feedback = []
cart = []

# ---------------------------
# Product Model
# ---------------------------

class Product(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool


# ---------------------------
# Day 1 - Get All Products
# ---------------------------

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# ---------------------------
# Filter Products
# ---------------------------

@app.get("/products/filter")
def filter_products(
    category: Optional[str] = Query(None),
    max_price: Optional[int] = Query(None),
    min_price: Optional[int] = Query(None)
):

    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return {"filtered_products": result}


# ---------------------------
# Get Product Price
# ---------------------------

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {"name": product["name"], "price": product["price"]}

    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------------
# Product Audit
# ---------------------------

@app.get("/products/audit")
def product_audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["in_stock"]]
    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


# ---------------------------
# Category Discount
# ---------------------------

@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    if discount_percent < 1 or discount_percent > 99:
        raise HTTPException(status_code=400, detail="discount_percent must be between 1 and 99")

    updated = []

    for product in products:
        if product["category"].lower() == category.lower():

            new_price = int(product["price"] * (1 - discount_percent / 100))
            product["price"] = new_price

            updated.append({
                "name": product["name"],
                "new_price": new_price
            })

    if not updated:
        return {"message": f"No products found in category '{category}'"}

    return {
        "updated_count": len(updated),
        "products": updated
    }


# ---------------------------
# Add Product
# ---------------------------

@app.post("/products", status_code=201)
def add_product(product: Product):

    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {"message": "Product added", "product": new_product}


# ---------------------------
# Update Product
# ---------------------------

@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = None,
    in_stock: Optional[bool] = None
):

    for product in products:

        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {"message": "Product updated", "product": product}

    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------------
# Delete Product
# ---------------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": f"Product '{product['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------------
# Place Single Order
# ---------------------------

class OrderRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=10)


@app.post("/orders")
def place_order(order: OrderRequest):

    product = next((p for p in products if p["id"] == order.product_id), None)

    if not product:
        return {"error": "Product not found"}

    if not product["in_stock"]:
        return {"error": "Product is out of stock"}

    order_data = {
        "order_id": len(orders) + 1,
        "product": product["name"],
        "quantity": order.quantity,
        "total_price": product["price"] * order.quantity,
        "status": "pending"
    }

    orders.append(order_data)

    return {"message": "Order placed successfully", "order": order_data}


# ---------------------------
# Customer Feedback
# ---------------------------

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }


# ---------------------------
# Product Summary
# ---------------------------

@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {"name": expensive["name"], "price": expensive["price"]},
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "categories": categories
    }


# ---------------------------
# BULK ORDER
# ---------------------------

class OrderItem(BaseModel):
    product_id: int
    quantity: int


class BulkOrder(BaseModel):
    company_name: str
    contact_email: str
    items: List[OrderItem]


@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})

        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": "Out of stock"})

        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }


# ==================================================
# DAY 5 CART SYSTEM
# ==================================================

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


def calculate_total(product, quantity):
    return product["price"] * quantity


# ---------------------------
# Add to Cart
# ---------------------------

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    for item in cart:

        if item["product_id"] == product_id:

            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])

            return {"message": "Cart updated", "cart_item": item}

    subtotal = calculate_total(product, quantity)

    cart_item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }

    cart.append(cart_item)

    return {"message": "Added to cart", "cart_item": cart_item}


# ---------------------------
# View Cart
# ---------------------------

@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# ---------------------------
# Remove From Cart
# ---------------------------

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"{item['product_name']} removed from cart"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# ---------------------------
# Checkout
# ---------------------------

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    orders_placed = []

    for item in cart:

        order_data = {
            "order_id": len(orders) + 1,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }

        orders.append(order_data)
        orders_placed.append(order_data)

    grand_total = sum(o["total_price"] for o in orders_placed)

    cart.clear()

    return {
        "message": "Checkout successful",
        "orders_placed": orders_placed,
        "grand_total": grand_total
    }


# ---------------------------
# Get All Orders
# ---------------------------

@app.get("/orders")
def get_orders():

    return {
        "orders": orders,
        "total_orders": len(orders)
    }