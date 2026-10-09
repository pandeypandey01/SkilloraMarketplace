import os
import uuid
from flask import Flask, request, jsonify, make_response
from tut4.models import Order
from tut4 import store
from tut4.errors import problem
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://localhost:5001")

# Swagger setup
SWAGGER_URL = "/api-docs"
API_URL = "/openapi.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Skillora Orders Service"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/openapi.yaml")
def openapi_spec():
    # Serve the spec file from the tut4 directory
    return app.send_static_file("openapi.yaml")

# ---------------- Existing routes ---------------- #

@app.after_request
def common_headers(response):
    response.headers.setdefault("Content-Type", "application/json; charset=utf-8")
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "99"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Idempotency-Key, If-Match, If-None-Match"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
    return response

@app.route("/orders", methods=["OPTIONS"])
def orders_options():
    r = make_response("", 204)
    r.headers["Allow"] = "GET, POST, OPTIONS"
    return r

@app.route("/orders", methods=["POST"])
def create_order():
    if not request.headers.get("Authorization"):
        return problem("unauthorized", "Unauthorized", 401, "Authorization header is required.")
    body = request.get_json(silent=True)
    if not body:
        return problem("bad-request", "Bad Request", 400, "Request body must be JSON.")

    # Validation
    errors = []
    if not body.get("customerId"):
        errors.append({"field": "customerId", "message": "required"})
    if not body.get("address"):
        errors.append({"field": "address", "message": "required"})
    if not isinstance(body.get("items"), list) or not body["items"]:
        errors.append({"field": "items", "message": "non-empty list required"})
    if errors:
        return problem("validation-error", "Validation failed", 422, "Request contains invalid fields.", errors)

    order_id = f"ORD-{uuid.uuid4().hex[:8]}"
    total = sum(float(item.get("qty", 1)) * 100.0 for item in body["items"])
    order = Order(order_id, body["customerId"], body["address"], body["items"], total=total)
    store.create(order)

    r = jsonify(order.as_json())
    r.status_code = 201
    r.headers["Location"] = f"/orders/{order_id}"
    return r

@app.route("/orders", methods=["GET"])
def list_orders():
    if not request.headers.get("Authorization"):
        return problem("unauthorized", "Unauthorized", 401, "Authorization header is required.")
    customer = request.args.get("customer")
    status = request.args.get("status")
    values = store.all()
    if customer:
        values = [o for o in values if o.customer_id == customer]
    if status:
        values = [o for o in values if o.status == status]
    return jsonify([o.as_json() for o in values])

@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    if not request.headers.get("Authorization"):
        return problem("unauthorized", "Unauthorized", 401, "Authorization header is required.")
    order = store.get(order_id)
    if not order:
        return problem("order-not-found", "Order not found", 404, "No order exists for this id.")
    return jsonify(order.as_json())

@app.route("/orders/<order_id>", methods=["PATCH"])
def update_order(order_id):
    if not request.headers.get("Authorization"):
        return problem("unauthorized", "Unauthorized", 401, "Authorization header is required.")
    order = store.get(order_id)
    if not order:
        return problem("order-not-found", "Order not found", 404, "No order exists for this id.")
    body = request.get_json(silent=True)
    if not body or body.get("status") not in {"pending", "confirmed", "completed", "cancelled"}:
        return problem("validation-error", "Validation failed", 422, "status must be a supported value.")
    order.status = body["status"]
    order.version += 1
    return jsonify(order.as_json())

@app.route("/orders/<order_id>/cancellation", methods=["POST"])
def cancel_order(order_id):
    if not request.headers.get("Authorization"):
        return problem("unauthorized", "Unauthorized", 401, "Authorization header is required.")
    order = store.get(order_id)
    if not order:
        return problem("order-not-found", "Order not found", 404, "No order exists for this id.")
    if order.status in {"completed", "cancelled"}:
        return problem("illegal-transition", "Illegal transition", 409, "Order cannot be cancelled in its current state.")
    order.status = "cancelled"
    order.version += 1
    return jsonify(order.as_json())

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("🚀 Starting Skillora Orders Service on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
