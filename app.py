from flask import Flask, jsonify, request

app=Flask(__name__)

store = [
  {"name": 'Store 1',
  "items": [{"name": "Item 1", "price": 18.99, "sold": False}]}
]

@app.route('/store/<string:name>')
def get_store(name):
  for x in store:
    if x["name"] == name:
      return jsonify(x)
  return jsonify({"msg": "Store not found"})


@app.route('/store')
def get_stores():
  return {'stores': store}

@app.route('/store/<string:name>/item')
def get_store_item(name):
  for x in store:
    if x["name"] == name:
      return jsonify({"items": x["items"]})
  return jsonify({"msg": "No store with the specified name"})

@app.route('/store', methods=['POST'])
def add_store():
  req_body = request.get_json()
  new_store = {"name": req_body["name"], "items": []}
  store.append(new_store)
  return jsonify(new_store)


@app.route('/store/<string:name>/item', methods=['POST'])
def add_store_item(name):
  for x in store:
    if x["name"] == name:
      req_body = request.get_json()
      x["items"].append(req_body["item"])
      return jsonify(x)
    return jsonify({"msg": "Store not found"})



app.run(port=5000)