import json
import requests

API_URI = "http://www.themealdb.com/api/json/v1/1/"


def get_meal_categories():
    # result = requests.get(API_URI + "categories.php")
    # categories = json.loads(result.text)
    # return [cat["strCategory"] for cat in categories["categories"]]
    # No reason to make the call each time.
    return [
        "Beef",
        "Chicken",
        "Dessert",
        "Lamb",
        "Miscellaneous",
        "Pasta",
        "Pork",
        "Seafood",
        "Side",
        "Starter",
        "Vegan",
        "Vegetarian",
        "Breakfast",
        "Goat",
    ]


def filter_by_category(category: str):
    result = requests.get(API_URI + "filter.php?c=" + category)
    meals = json.loads(result.text)
    if not meals["meals"]:
        return {}
    return {meal["strMeal"]: meal["idMeal"] for meal in meals["meals"]}


def lookup_meal_by_id(id: str):
    result = requests.get(API_URI + "lookup.php?i=" + id)
    return json.loads(result.text)["meals"][0]


def filter_by_ingredient(ingredient: str):
    ingredient = ingredient.replace(" ", "_")
    result = requests.get(API_URI + "filter.php?i=" + ingredient)
    meals = json.loads(result.text)
    if not meals["meals"]:
        return {}
    return {meal["strMeal"]: meal["idMeal"] for meal in meals["meals"]}
