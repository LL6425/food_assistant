import inspect
from abc import abstractmethod
from typing import Tuple, Dict, Type

from pydantic import BaseModel

from src.conf.data_model.llm import StructOutput
from src.conf.data_model.output import Recipe, Text


class Tool(StructOutput):
    name: str = None
    description: str = None

    def __init__(self):
        StructOutput.__init__(self)

        assert isinstance(self.name, str), "Name must be a string."
        assert isinstance(self.description, str), "Description must be a string."

        self.input_model, self.input_schema = self.get_input_structure()

    @abstractmethod
    def __call__(self, inp: BaseModel):
        pass

    def get_input_structure(self) -> Tuple[Type[BaseModel], Dict]:
        parameters = inspect.signature(self.__call__).parameters

        assert (
            list(parameters.keys()) == ["inp"]
        ), "Tool call method must follow the (self, inp: BaseModel) arguments convention"

        input_model: BaseModel = parameters["inp"].annotation

        return input_model, input_model.model_json_schema()


class ToolLLM(Tool):
    def __init__(self, client, model: str):
        Tool.__init__(self)

        self.client = client
        self.model = model

    def __call__(self, inp: BaseModel):
        pass


class RecipeSuggest(ToolLLM):
    description = "Tool designed to suggest recipes"
    name = "recipe_suggest"
    output_structure = Recipe

    def __init__(self, client, model: str):
        ToolLLM.__init__(self, client=client, model=model)

    @abstractmethod
    def __call__(self, inp: Text) -> Recipe:
        pass


class ChatBot(ToolLLM):
    description = "Tool designed to provide generic food related answers"
    name = "food_chatbot"
    output_structure = Text

    def __init__(self, client, model: str):
        ToolLLM.__init__(self, client=client, model=model)

    @abstractmethod
    def __call__(self, inp: Text) -> Text:
        pass
