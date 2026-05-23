from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

# =========================
# GAME STATE
# =========================
game_state = {
    "title": "NEON MARKET",
    "credits": 1000,
    "inventory": {
        "Data Cubes": 0,
        "Fuel": 0,
        "Data Shards": 0,
    },
    "market": {
        "Data Cubes": {"price": 120, "history": [120]},
        "Fuel": {"price": 75, "history": [75]},
        "Data Shards": {"price": 25, "history": [25]}
    },
    "message": "Market connected...",
    "color": "#00ff99"
}

def update_market():
    for item in game_state["market"]:
        current_price = game_state["market"][item]["price"]
        # Random fluctuation
        change = random.randint(-25, 25)
        new_price = max(10, current_price + change)
        
        game_state["market"][item]["price"] = new_price
        
        # Keep track of history for the graph (last 10 prices)
        game_state["market"][item]["history"].append(new_price)
        if len(game_state["market"][item]["history"]) > 10:
            game_state["market"][item]["history"].pop(0)

@app.route("/")
def index():
    return render_template("index.html", data=game_state)

@app.route("/wait", methods=["POST"])
def wait():
    update_market()
    game_state["message"] = "A day passes... prices updated."
    game_state["color"] = "#00e1ff"
    return redirect("/")

@app.route("/buy/<item>", methods=["POST"])
def buy(item):
    try:
        qty = int(request.form.get("quantity", 1))
    except ValueError:
        qty = 1

    price_per_unit = game_state["market"][item]["price"]
    total_cost = price_per_unit * qty

    if game_state["credits"] >= total_cost:
        game_state["credits"] -= total_cost
        game_state["inventory"][item] += qty
        game_state["message"] = f"Purchased {qty} {item} for {total_cost} CR."
        game_state["color"] = "#00ff99"
    else:
        game_state["message"] = "INSUFFICIENT CREDITS"
        game_state["color"] = "#ff003c"
    return redirect("/")

@app.route("/sell/<item>", methods=["POST"])
def sell(item):
    try:
        qty = int(request.form.get("quantity", 1))
    except ValueError:
        qty = 1

    if game_state["inventory"][item] >= qty:
        price = game_state["market"][item]["price"]
        game_state["inventory"][item] -= qty
        game_state["credits"] += (price * qty)
        game_state["message"] = f"Sold {qty} {item} for {price * qty} CR."
        game_state["color"] = "#00ff99"
    else:
        game_state["message"] = f"Not enough {item} to sell."
        game_state["color"] = "#ff003c"
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)