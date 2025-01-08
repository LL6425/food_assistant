import json
from abc import ABC, abstractmethod
from typing import List, Callable, Iterable, Dict, Tuple, Type

from pydantic import BaseModel

from src.conf.data_model.llm import Guardian, StructOutput
from src.prompt.system import SystemPrompt
from src.conf.data_model.tools import Tool, ToolLLM
from src.conf.exceptions import UnsupportedOperationError
from src.conf.data_model.pipeline import Pipeline


class FoodAssistant(StructOutput):
    output_structure: Type[BaseModel] = Pipeline

    def __init__(
        self,
        api_key: str,
        system: SystemPrompt,
        guardian: Guardian,
        model: str,
        tools: Iterable[Type[Tool]] = None,
    ):
        StructOutput.__init__(self)
        self.client = self._get_client(api_key=api_key)
        self.model = model

        self.guardian = guardian

        self.tools_info, self.tools_d = self._prepare_tools(tools=tools)

        self.history = [{"role": "system", "content": system.system_description}]

    @abstractmethod
    def _get_client(self, api_key: str):
        pass

    def _prepare_tools(
        self, tools: Iterable[Type[Tool]]
    ) -> Tuple[List[Dict[str, str]], Dict[str, Tool]]:
        tools_info, tools_d = [], {}

        for tool in tools:
            tool_object = (
                tool(client=self.client, model=self.model)
                if issubclass(tool, ToolLLM)
                else tool()
            )

            tools_info.append(
                {
                    "name": tool_object.name,
                    "description": tool_object.description,
                    "input": tool_object.input_schema,
                }
            )

            tools_d[tool_object.name] = tool_object

        return tools_info, tools_d

    def _provide_tools(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return history + [
            {
                "role": "system",
                "content": f"The following tools are provided: {json.dumps(self.tools_info, indent=self.indent)}",
            }
        ]

    def _guard(self, prompt: str):
        if not self.guardian.validate(
            client=self.client, model=self.model, history=self.history, prompt=prompt
        ):
            raise UnsupportedOperationError("The request is not food related.")
