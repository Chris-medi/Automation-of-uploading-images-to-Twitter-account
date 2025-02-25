from langchain_ollama import OllamaLLM, ChatOllama
import random

from src.utils.image import getModels, getSamplingMethods
from src.LLM.schemas import PromptSchemaResponse
from src.LLM.templates import prompt_template_to_llm, prompt_template_to_improve
from settings.config import topics_images, ENV

llm = OllamaLLM(
  model="phi4",
  temperature=1.0,
  base_url="192.168.1.9:11434",
  # other params ...
)

llm_status = OllamaLLM(
  model="phi4",
  temperature=0.5,
  base_url="192.168.1.9:11434",
  format="json"
  # other params ...
)

llm_parser = ChatOllama(
  model="llama3.2:3b",
  temperature=0.1,
  base_url="192.168.1.9:11434",
  format="json"
  # other params ...
)


def generatePromptToCreateImage(input):
  models = getModels()
  sampling_methos = getSamplingMethods()
  chain = prompt_template_to_llm | llm
  answer = chain.invoke({"input": input, "models": models,"sampler_name":sampling_methos})
  return answer

def refineAndEstructuredPrompt(prompt):
  print(prompt)
  structured_output_llm = llm_parser.with_structured_output(PromptSchemaResponse)
  chain = prompt_template_to_improve | structured_output_llm
  return chain.invoke({"input": prompt})

class SettingsLlm:
  def __init__(self):
    self.base_url = ENV['BASE_URL_OLLAMA']

class LlmModelGenerator(SettingsLlm):
  def __init__(self, model, temperature=0.1):
    self.llm = OllamaLLM(
      model=model,
      temperature=temperature,
      base_url=self.base_url,
    )

class GenerateGoodTheme:
  def __init__(self):
    self._topics = topics_images['topics']
    self._concepts = topics_images['concepts']

  def randomTopic(self, choose=1):
    topic = random.sample(self._topics,choose)
    return ", ".join(topic)

  def randomConcept(self, choose=1):
    concept = random.sample(self._concepts, choose)
    return ", ".join(concept)


class GeneratePrompt(GenerateGoodTheme):
  template = """
    Generate a prompt to create an image about ** {concept} ** and {topic}.
    The scene should evoke a sense of wonder and serenity, with intricate details that make it feel alive.
    Let your creativity guide the elements, such as the type of terrain, lighting, weather, and atmosphere.
    Focus on achieving a photorealistic style with stunning attention to detail, vibrant colors, and lifelike textures.
    The final result should be a masterpiece that Capture the beauty and magic of related topics in their purest form in one image.
  """
  def create(self):
    concept = self.randomConcept(1)
    topic = self.randomTopic(3)
    return self.template.format(concept=concept, topic=topic)

async def generatedStatus(idea):
  # generamos un status a con los temas selecionados y un prompt inicial de GeneratePrompt
  prompt = f"""
  Give a status to publish on the Twitter account with the hashtag and icons of
  this idea {idea} the status is that it is not too long (no more than 100 characters the status) must be in English and a prompt.
  The response must be a json with these keys "status","prompt"
  """
  return llm_status.invoke(prompt)
