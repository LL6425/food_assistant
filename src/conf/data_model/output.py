from typing import Union

from pydantic import BaseModel, Field
    
class Text(BaseModel):

    text: str = Field(description="Simple text")

class Ingredient(BaseModel):
    name: str
    quantity: Union[float, str]
    unit: str

class Recipe(BaseModel):
    name: str
    ingredients: list[Ingredient]
    procedure: list[str]
    cuisine: str = Field(description="Cuisine of origin of the recipe")
    execution_time: int = Field(description="Execution time in minutes")




