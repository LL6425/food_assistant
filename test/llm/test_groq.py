import os

import pytest

from src.llm import GroqGuardian
from src.prompt.guardian import GuardianPrompt

def test_groq_guardian():

    guardian_prompt = GuardianPrompt()

    guardian = GroqGuardian(groq_api_key=os.environ['GROQ_API_KEY'], prompt=guardian_prompt)

    assert guardian.validate('Provide lasagne recipe')
    assert not guardian.validate('Code hello world in python')





