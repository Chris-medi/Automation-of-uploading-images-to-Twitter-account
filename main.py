from langgraph.errors import GraphRecursionError
import asyncio

from src.utils.image import requestStableDifusion, createPayload
from src.LLM.ollama  import generatePromptToCreateImage, \
GeneratePrompt, generatedStatus, refineAndEstructuredPrompt
from src.LLM.graph import graph
from src.utils.twitter import postTweet

generate_prompt = GeneratePrompt()

async def main():
  try:

    config = {"configurable": {"thread_id": "1"},"recursion_limit": 5}

    answer = await graph.ainvoke(
      {"idea": generate_prompt.create() },
      config
    )

    print(answer['status'])
    requestStableDifusion(createPayload(answer['prompt']))
    value = input('Desea publica en twitter esta imagen: \n')
    if value.lower() in ('si','claro','yes'):
      print('publicando ...')
      # postTweet("Unveiling a digital masterpiece: #ForestCyberpunkNight 🌿⚡️🎨","output_images/image_64d8b073-a4f0-4b02-8dd2-eff0cdec7947.png")
      print('Publicado!')
  except GraphRecursionError :
    print('ha superado el numero de recursiones')
  except Exception as e:
    print(e)
    print('error inesperado')

if __name__ == "__main__":
  asyncio.run(main())
