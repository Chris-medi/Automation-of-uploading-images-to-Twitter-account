from langchain_ollama import OllamaLLM, ChatOllama
import random


from src.utils.image import getModels, getSamplingMethods
from src.LLM.schemas import PromptSchemaResponse
from src.LLM.templates import prompt_template_to_llm, prompt_template_to_improve
from settings.config import topics_images, ENV

class SettingsLlm:
  base_url = ENV['BASE_URL_OLLAMA']

  def getLLM(self):
    return self.llm

class LlmModelOllama(SettingsLlm) :
  def __init__(self, model:str, temperature=0.1, **kwargs):
    self.llm = OllamaLLM(
      model=model,
      temperature=temperature,
      base_url=self.base_url,
      **kwargs
    )

class ChatModelOllama(SettingsLlm):
  def __init__(self, model:str, temperature=0.1, **kwargs):
    self.llm = ChatOllama(
      model=model,
      temperature=temperature,
      base_url=self.base_url,
      **kwargs
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
  template = """Generate a prompt to create an image about ** {concept} ** and {topic}.
    The scene should evoke a sense of wonder and serenity, with intricate details that make it feel alive.
    Let your creativity guide the elements, such as the type of terrain, lighting, weather, and atmosphere.
    Focus on achieving a photorealistic style with stunning attention to detail, vibrant colors, and lifelike textures.
    The final result should be a masterpiece that Capture the beauty and magic of related topics in their purest form in one image."""
  def create(self):
    concept = self.randomConcept(1)
    topic = self.randomTopic(3)
    return self.template.format(concept=concept, topic=topic)

async def generatedStatus(idea):
  # generamos un status a con los temas selecionados y un prompt inicial de GeneratePrompt
  llm = LlmModelOllama('phi4', 0.5, format="json").getLLM()
  prompt = f"""Give a status to publish on the Twitter account with the hashtag and icons of
  this idea {idea} the status is that it is not too long (no more than 100 characters the status) must be in English and a prompt.
  The response must be a json with these keys "status","prompt". """
  return llm.invoke(prompt)

async def generatePromptToCreateImage(prompt):
  models = getModels()
  sampling_methos = getSamplingMethods()
  llm = LlmModelOllama('phi4',1.0).getLLM()
  chain = prompt_template_to_llm | llm
  answer = chain.invoke({"input": prompt, "models": models,"sampler_name":sampling_methos})
  return answer

async def refineAndEstructuredPrompt(prompt):
  llm = ChatModelOllama('llama3.2:3b', format="json").getLLM()
  structured_output_llm = llm.with_structured_output(PromptSchemaResponse)
  chain = prompt_template_to_improve | structured_output_llm
  answer = chain.invoke({"input": prompt})
  return answer

