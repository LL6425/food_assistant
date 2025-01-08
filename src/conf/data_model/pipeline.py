from typing import List, Dict

from pydantic import BaseModel, Field

from src.conf.data_model.tools import Tool

class Pipeline(BaseModel):

    pipeline_input: Dict = Field(description="Pipeline input, consistent with first tool required input")
    tool_calls: List[str] = Field(description="List of tools in the order they have to be called")

    def execute(self, tools_d: Dict[str, Tool]):

        answer = tools_d.get(self.tool_calls[0]).input_model.model_validate(self.pipeline_input)

        for tc in self.tool_calls:

            answer = tools_d.get(tc)(answer)

        return answer