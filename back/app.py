import json
from pathlib import Path

import mdl
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

CARS_FILE = Path("cars.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cars", methods=["GET"])
def cars():
    cars = mdl.get_cars(CARS_FILE)
    if len(cars) == 0:
        msg = "Car list is empty, go ahead and add a new car..."
        flash(msg, "info")
        h2str = ""
    else:
        h2str = "Cars:"
    return render_template("cars.html", cars=cars, h2str=h2str)


@app.route("/search", methods=["GET", "POST"])
def search():
    # Implement logic for searching cars
    if request.method == "GET":
        return render_template("search.html")
    key = request.form["key"]
    val = request.form["val"]
    cars = mdl.get_cars(CARS_FILE)
    search_results = [car for car in cars if car.get(key) == val]
    if len(search_results) == 0:
        msg = "No result"
        flash(msg, "warning")
    return render_template("search.html", cars=search_results)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    # Implement logic for adding a car
    cars: list[dict] = []
    make = request.form["make"]
    model = request.form["model"]
    year = request.form["year"]
    car = {"make": make, "model": model, "year": year}
    cars.append(car)
    cars = mdl.get_cars(CARS_FILE) + cars

    with open("cars.json", "w") as file:
        json.dump(cars, file, indent=2)

    flash(f"{make} {model} {year} added successfully", "success")
    # return render_template("cars.html", cars=cars) post post error
    # follow prg post redirect get...
    # Redirect to the /cars endpoint (GET) instead of rendering the template directly
    return redirect(url_for("cars"))


@app.route("/update", methods=["GET", "POST"])
def update():
    # Implement logic for updating a car
    cars = mdl.get_cars(CARS_FILE)
    if request.method == "GET":
        if len(cars) > 0:
            # return render_template("update.html", cars=cars, enumerate=enumerate, len=len)
            return render_template("update.html", cars=cars)
        # if len(cars == 0)
        return redirect(url_for("cars"))

    idx = request.form["idx"]
    key = request.form["key"]
    val = request.form["val"]

    cars = mdl.update_car(cars, idx, key, val)
    with open(CARS_FILE, "w") as file:
        json.dump(cars, file, indent=2)

    return render_template("update.html", cars=cars, idx=idx, int=int)


from flask import jsonify, render_template, request


@app.route("/delete", methods=["GET", "POST"])
def delete():
    # Get the list of cars
    cars = mdl.get_cars(CARS_FILE)

    if request.method == "GET":
        if len(cars) == 0:
            flash_msg = "Car list is empty, go ahead and add a new car..."
            category = "info"
        else:
            flash_msg = "Note: Delete action is irreversible and cannot be undone."
            category = "danger"
        flash(flash_msg, category)

        # Display the delete.html template with the car list
        return render_template("delete.html", cars=cars)

    elif request.method == "POST":
        # Handle the deletion logic
        idx = request.form.get("idx")

        if idx is not None:
            # Delete the car at the specified index
            del cars[int(idx)]

            # Update the cars.json file
            with open(CARS_FILE, "w") as file:
                json.dump(cars, file, indent=2)

        # Redirect to the /delete endpoint (GET) to refresh the page
        return redirect(url_for("delete"))


if __name__ == "__main__":
    app.run(debug=True)
