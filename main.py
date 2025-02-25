from pydantic import ValidationError
import asyncio
import orjson
from operator import itemgetter

from src.utils.image import requestStableDifusion, createPayload
from src.LLM.ollama  import generatePromptToCreateImage, \
GeneratePrompt, generatedStatus, refineAndEstructuredPrompt
from src.LLM.graph import graph

generate_prompt = GeneratePrompt()

async def main():
  try:
    # user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
    # config = {"configurable": {"thread_id": "1"}}

    # events = graph.stream(
    #   {"messages": [{"role": "user", "content": user_input}]},
    #   config,
    #   stream_mode="values",
    # )
    # for event in events:
    #     if "messages" in event:
    #         event["messages"][-1].pretty_print()
    prompt_step_one = await generatedStatus(generate_prompt.create())
    status, prompt = itemgetter('status','prompt')(orjson.loads(prompt_step_one))
    print(status)
    print(prompt)
    prompt_refine = refineAndEstructuredPrompt(generatePromptToCreateImage(prompt))
    requestStableDifusion(createPayload(prompt_refine.model_dump()))
    value = input('Desea publica en twitter esta imagen: \n')
    if value.lower() in ('si','claro','yes'):
      print('publicando ...')
      print('Publicado!')
  except ValidationError as e:
    print(e)

if __name__ == "__main__":
  asyncio.run(main())
