from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)

PRESET_PRODUCTS = [
 {"name": "Orange Juice (1L)", "amount": 1.0},
 {"name": "Apple Juice (1L)", "amount": 1.0},
 {"name": "Milk Carton (1L)", "amount": 1.0},
 {"name": "Water Bottle (0.5L)", "amount": 0.5},
 {"name": "Soda Can (0.33L)", "amount": 0.33},
 {"name": "Juice Box (6-pack)", "amount": 6.0},
 {"name": "Beer Crate (24-pack)", "amount": 24.0},
]


def get_preset_products():
 return PRESET_PRODUCTS


class WarehouseStore:
 def __init__(self):
  self.warehouses = {}
  self.counter = 0

 def get_next_id(self):
  self.counter += 1
  return self.counter

 def reset(self):
  self.warehouses = {}
  self.counter = 0

 def get_all(self):
  return self.warehouses

 def get(self, warehouse_id):
  return self.warehouses.get(warehouse_id)

 def create(self, name, capacity, initial_balance=0):
  warehouse_id = self.get_next_id()
  varasto = Varasto(capacity, initial_balance)
  entry = {"id": warehouse_id, "name": name, "varasto": varasto}
  self.warehouses[warehouse_id] = entry
  return warehouse_id

 def update_name(self, warehouse_id, name):
  if warehouse_id in self.warehouses:
   self.warehouses[warehouse_id]["name"] = name
   return True
  return False

 def delete(self, warehouse_id):
  if warehouse_id in self.warehouses:
   del self.warehouses[warehouse_id]
   return True
  return False

 def add_content(self, warehouse_id, amount):
  warehouse = self.get(warehouse_id)
  if warehouse:
   warehouse["varasto"].lisaa_varastoon(amount)
   return True
  return False

 def take_content(self, warehouse_id, amount):
  warehouse = self.get(warehouse_id)
  if warehouse:
   return warehouse["varasto"].ota_varastosta(amount)
  return 0.0


store = WarehouseStore()


def reset_warehouses():
 store.reset()


def get_all_warehouses():
 return store.get_all()


def get_warehouse(warehouse_id):
 return store.get(warehouse_id)


def create_warehouse(name, capacity, initial_balance=0):
 return store.create(name, capacity, initial_balance)


def update_warehouse_name(warehouse_id, name):
 return store.update_name(warehouse_id, name)


def delete_warehouse(warehouse_id):
 return store.delete(warehouse_id)


def add_to_warehouse(warehouse_id, amount):
 return store.add_content(warehouse_id, amount)


def take_from_warehouse(warehouse_id, amount):
 return store.take_content(warehouse_id, amount)


@app.route("/")
def index():
 return render_template("index.html", warehouses=get_all_warehouses())


@app.route("/create", methods=["GET", "POST"])
def create():
 if request.method == "POST":
  name = request.form.get("name", "").strip()
  capacity = float(request.form.get("capacity", 0))
  initial = float(request.form.get("initial", 0))
  create_warehouse(name, capacity, initial)
  return redirect(url_for("index"))
 return render_template("create.html")


@app.route("/edit/<int:warehouse_id>", methods=["GET", "POST"])
def edit(warehouse_id):
 warehouse = get_warehouse(warehouse_id)
 if not warehouse:
  return redirect(url_for("index"))
 if request.method == "POST":
  name = request.form.get("name", "").strip()
  update_warehouse_name(warehouse_id, name)
  return redirect(url_for("index"))
 return render_template("edit.html", warehouse=warehouse)


@app.route("/add/<int:warehouse_id>", methods=["GET", "POST"])
def add(warehouse_id):
 warehouse = get_warehouse(warehouse_id)
 if not warehouse:
  return redirect(url_for("index"))
 if request.method == "POST":
  amount = float(request.form.get("amount", 0))
  add_to_warehouse(warehouse_id, amount)
  return redirect(url_for("index"))
 return render_template(
  "add.html",
  warehouse=warehouse,
  products=get_preset_products()
 )


@app.route("/take/<int:warehouse_id>", methods=["GET", "POST"])
def take(warehouse_id):
 warehouse = get_warehouse(warehouse_id)
 if not warehouse:
  return redirect(url_for("index"))
 if request.method == "POST":
  amount = float(request.form.get("amount", 0))
  take_from_warehouse(warehouse_id, amount)
  return redirect(url_for("index"))
 return render_template("take.html", warehouse=warehouse)


@app.route("/delete/<int:warehouse_id>", methods=["POST"])
def delete(warehouse_id):
 delete_warehouse(warehouse_id)
 return redirect(url_for("index"))


if __name__ == "__main__":
 app.run()
