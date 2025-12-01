import unittest
from app import (
    app, reset_warehouses, create_warehouse, get_warehouse,
    get_all_warehouses, update_warehouse_name, delete_warehouse,
    add_to_warehouse, take_from_warehouse
)


class TestAppHelpers(unittest.TestCase):
    def setUp(self):
        reset_warehouses()

    def test_create_warehouse(self):
        warehouse_id = create_warehouse("Test", 100, 50)
        self.assertEqual(warehouse_id, 1)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["name"], "Test")
        self.assertEqual(warehouse["varasto"].tilavuus, 100)
        self.assertEqual(warehouse["varasto"].saldo, 50)

    def test_get_all_warehouses(self):
        create_warehouse("First", 100)
        create_warehouse("Second", 200)
        warehouses = get_all_warehouses()
        self.assertEqual(len(warehouses), 2)

    def test_get_nonexistent_warehouse(self):
        warehouse = get_warehouse(999)
        self.assertIsNone(warehouse)

    def test_update_warehouse_name(self):
        warehouse_id = create_warehouse("Old Name", 100)
        result = update_warehouse_name(warehouse_id, "New Name")
        self.assertTrue(result)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["name"], "New Name")

    def test_update_nonexistent_warehouse(self):
        result = update_warehouse_name(999, "Name")
        self.assertFalse(result)

    def test_delete_warehouse(self):
        warehouse_id = create_warehouse("To Delete", 100)
        result = delete_warehouse(warehouse_id)
        self.assertTrue(result)
        self.assertIsNone(get_warehouse(warehouse_id))

    def test_delete_nonexistent_warehouse(self):
        result = delete_warehouse(999)
        self.assertFalse(result)

    def test_add_to_warehouse(self):
        warehouse_id = create_warehouse("Test", 100, 0)
        result = add_to_warehouse(warehouse_id, 50)
        self.assertTrue(result)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["varasto"].saldo, 50)

    def test_add_to_nonexistent_warehouse(self):
        result = add_to_warehouse(999, 50)
        self.assertFalse(result)

    def test_take_from_warehouse(self):
        warehouse_id = create_warehouse("Test", 100, 50)
        taken = take_from_warehouse(warehouse_id, 30)
        self.assertEqual(taken, 30)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["varasto"].saldo, 20)

    def test_take_from_nonexistent_warehouse(self):
        taken = take_from_warehouse(999, 50)
        self.assertEqual(taken, 0.0)


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        reset_warehouses()

    def test_index_empty(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)
        self.assertIn(b"No warehouses yet", response.data)

    def test_index_with_warehouses(self):
        create_warehouse("Test Warehouse", 100, 50)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)

    def test_create_get(self):
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create New Warehouse", response.data)

    def test_create_post(self):
        response = self.client.post("/create", data={
            "name": "New Warehouse",
            "capacity": "100",
            "initial": "25"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"New Warehouse", response.data)

    def test_edit_get(self):
        warehouse_id = create_warehouse("Edit Test", 100)
        response = self.client.get(f"/edit/{warehouse_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Warehouse", response.data)

    def test_edit_nonexistent(self):
        response = self.client.get("/edit/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)

    def test_edit_post(self):
        warehouse_id = create_warehouse("Old Name", 100)
        response = self.client.post(f"/edit/{warehouse_id}", data={
            "name": "Updated Name"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Name", response.data)

    def test_add_get(self):
        warehouse_id = create_warehouse("Add Test", 100)
        response = self.client.get(f"/add/{warehouse_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add to Warehouse", response.data)

    def test_add_nonexistent(self):
        response = self.client.get("/add/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)

    def test_add_post(self):
        warehouse_id = create_warehouse("Add Test", 100, 0)
        response = self.client.post(f"/add/{warehouse_id}", data={
            "amount": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["varasto"].saldo, 50)

    def test_take_get(self):
        warehouse_id = create_warehouse("Take Test", 100, 50)
        response = self.client.get(f"/take/{warehouse_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Take from Warehouse", response.data)

    def test_take_nonexistent(self):
        response = self.client.get("/take/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)

    def test_take_post(self):
        warehouse_id = create_warehouse("Take Test", 100, 50)
        response = self.client.post(f"/take/{warehouse_id}", data={
            "amount": "30"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = get_warehouse(warehouse_id)
        self.assertEqual(warehouse["varasto"].saldo, 20)

    def test_delete(self):
        warehouse_id = create_warehouse("Delete Test", 100)
        response = self.client.post(
            f"/delete/{warehouse_id}",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(get_warehouse(warehouse_id))
