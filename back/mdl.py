import json

from flask import flash


def get_cars(CARS_FILE):
    cars: list(dict) = []
    if CARS_FILE.is_file():
        with open("cars.json", "r") as file:
            cars = json.load(file)
    return cars


# Function to update a specific key's value in a dictionary key: 'id'
# def update_car(list_of_dicts, target_id, key_to_update, new_value):
#     for d in list_of_dicts:
#         if d.get("id") == target_id:
#             d[key_to_update] = new_value
#             break


# Function to update a specific key's value in a dictionary by object index
def update_car(cars, idx, key, val):
    idx = int(idx) - 1  # Convert idx to an integer - 1 for real list indexing
    if 0 <= idx < len(cars):
        cars[idx][key] = val
        return cars
    return cars  # Add a return statement in case the condition is not met
