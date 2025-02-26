from langgraph.errors import GraphRecursionError
from typing import Any
import asyncio
import logging

from src.utils.image import requestStableDifusion, createPayload
from src.LLM.ollama  import generatePromptToCreateImage, \
GeneratePrompt, generatedStatus, refineAndEstructuredPrompt
from src.LLM.graph import graph
from src.utils.twitter import postTweet


logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  handlers=[
    logging.FileHandler('app.log'),
    logging.StreamHandler()
  ]
)

class ImageGenerator:
  def __init__(self):
    self.generate_prompt = GeneratePrompt()
    self.config = {
      "configurable": {"thread_id": "1"},
      "recursion_limit": 9
    }

  async def _generateImage(self) -> tuple[dict[str, Any], list[str]]:
    logging.info("Generating image...")

    idea = self.generate_prompt.create()
    answer = await graph.ainvoke(
      {"idea": idea},
      self.config
    )
    logging.info(f"Generated status: {answer['status']}")
    images_paths = requestStableDifusion(createPayload(answer['prompt']))
    logging.info(f"Image generated at: {images_paths}")
    return (answer, images_paths)

  def _handleTwitterPost(self, answer: dict[str, Any], path_image: list[str]) -> None:
    value = input('Do you want to publish this image on Twitter? (yes/no): ')
    if value.lower() in ('si', 'claro', 'yes', 'y'):
      logging.info("Publishing to Twitter...")
      try:
        postTweet(answer['status'], path_image[0])
        logging.info("Successfully published to Twitter!")
      except Exception as e:
        logging.error(f"Failed to post to Twitter: {str(e)}")

  async def generateAndPost(self) -> None:
    try:
      answer, images_paths = await self._generateImage()
      if answer:
          self._handleTwitterPost(answer, images_paths)
    except GraphRecursionError:
      logging.error("Maximum recursion limit reached")
    except Exception as e:
      logging.error(f"Unexpected error: {str(e)}")

async def main():
    generator = ImageGenerator()
    await generator.generateAndPost()

if __name__ == "__main__":
  asyncio.run(main())
