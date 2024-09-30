import pytest

from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.main import app as my_app
from app.schemas.v1.order import S_OrderFull, S_OrderPagination


client = TestClient(my_app)


# def test_order_list():
#     response = client.get("/api/v1/orders")
#     assert response.status_code == 200
#     assert response.json() == S_OrderPagination.model_json_schema()


# def test_create_order():
#     order_data = {
#         "items": [
#             {"product_id": 1, "quantity": 2}
#         ]
#     }
#     response = client.post("/api/v1/orders", json=order_data)
#     assert response.status_code == 201
#     assert response.json() == S_OrderFull.model_json_schema()


# def test_order_statuses():
#     response = client.get("/api/v1/orders/statuses")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_order_info_by_id():
#     response = client.get("/api/v1/orders/1")
#     assert response.status_code == 200
#     assert response.json() == S_OrderFull.model_json_schema()


# def test_update_order_status():
#     response = client.patch("/api/v1/orders/1/status", json={"status": "SHIPPING"})
#     assert response.status_code == 200
#     assert response.json() == S_OrderFull.model_json_schema()


# def test_create_order_no_items():
#     order_data = {
#         "items": []
#     }
#     response = client.post("/api/v1/orders", json=order_data)
#     assert response.status_code == 400
