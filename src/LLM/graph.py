
from operator import itemgetter

import orjson
from typing import Literal
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from pydantic import ValidationError

from src.LLM.ollama import generatedStatus, generatePromptToCreateImage, \
refineAndEstructuredPrompt

class State(TypedDict):
  idea: str
  prompt: str
  status: str


memory = MemorySaver()


async def createInitialIdea(state: State):
  prompt_step_one = await generatedStatus(state['idea'])
  status, prompt = itemgetter('status','prompt')(orjson.loads(prompt_step_one))
  return {"prompt": prompt, "status": status}

async def generateIdea(state: State):
  response = await  generatePromptToCreateImage(state['prompt'])
  return {"prompt": response}

async def refineIdea(state: State):
  try:
    response = await refineAndEstructuredPrompt(state['prompt'])
  except ValidationError :
    return "Error"
  return {"prompt": response.model_dump()}

async def conditionNodeRefinement(state: State) -> Literal["createInitialIdea", END]:
  if state['prompt'] == "Error":
    print('El modelo no genero correctamente la respuesta')
    return "createInitialIdea"
  else:
    print('El modelo genero correctamente la respuesta')
    return END

graph_builder = StateGraph(State)

graph_builder.add_node("createInitialIdea", createInitialIdea)
graph_builder.add_node("generateIdea", generateIdea)
graph_builder.add_node("refineIdea", refineIdea)

#
graph_builder.add_edge(START, "createInitialIdea")
graph_builder.add_edge("createInitialIdea", "generateIdea")
graph_builder.add_edge("generateIdea", "refineIdea")

graph_builder.add_conditional_edges("refineIdea", conditionNodeRefinement)


graph = graph_builder.compile(checkpointer=memory)

