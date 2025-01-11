from typing import Union
from abc import abstractmethod

from pydantic import BaseModel, Field


class Output(BaseModel):
    @abstractmethod
    def as_text(self) -> str:
        pass


class Text(Output):
    text: str = Field(description="Simple text")

    def as_text(self) -> str:
        return self.text


class Ingredient(BaseModel):
    name: str
    quantity: Union[float, int]
    unit: str


class Recipe(Output):
    name: str
    ingredients: list[Ingredient]
    procedure: list[str]
    cuisine: str = Field(description="Cuisine of origin of the recipe")
    execution_time: int = Field(description="Execution time in minutes")
    people: int = Field(description="Number of people the recipe is for")

    def as_text(self) -> str:
        ingredients = "\n".join(
            [
                f"- {ingredient.name}: {ingredient.quantity} {ingredient.unit}"
                for ingredient in self.ingredients
            ]
        )
        procedure = "\n".join(
            [f"{i+1}. {step}" for i, step in enumerate(self.procedure)]
        )
        t = f"""Name: {self.name} \nCuisine: {self.cuisine} \nExecution time: {self.execution_time} minutes \nPeople: {self.people} \nIngredients: \n{ingredients} \nProcedure: \n{procedure}"""
        return t
