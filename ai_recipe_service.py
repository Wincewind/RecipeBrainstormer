import json
from  os import getenv
import google.generativeai as genai
import typing_extensions as typing

genai.configure(api_key=getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")


class Categories(typing.TypedDict):
    categories: list[str]

class Recipes(typing.TypedDict):
    meals: list[str]

class Ingredient(typing.TypedDict):
    name: str
    amount: float
    measurement: str

class Recipe(typing.TypedDict):
    ingredients: list[Ingredient]


def get_meal_categories():
    result = model.generate_content(
    "List a few meal categories and diets.",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Categories
        )
    )
    return json.loads(result.parts[0].text)["categories"]

def find_meals(inc_terms: list, exc_terms: list):
    result = model.generate_content(
    f"List a few recipes that must belong to these categories/diets and use these ingredients: '{exc_terms}' but can also belong to these categories/diets or use these ingredients: '{inc_terms}'.",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Recipes
        )
    )
    return json.loads(result.parts[0].text)["meals"]

def find_ingredients(recipe_name: str):
    result = model.generate_content(
    f"Come up with ingredients for a recipe named: {recipe_name}.",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Recipe
        )
    )
    return json.loads(result.parts[0].text)["ingredients"]
