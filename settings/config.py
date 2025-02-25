from dotenv import dotenv_values
from pathlib import Path
import orjson

from settings.LLM import input_prompt, instructions_model_improve, instructions_model_llm

ENV = dotenv_values(".env")

topics_images = orjson.loads(Path('settings/topics-images.json').read_text(encoding='utf-8'))


