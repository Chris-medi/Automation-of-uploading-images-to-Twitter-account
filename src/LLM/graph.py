from operator import itemgetter
import orjson
from typing import Literal, Dict, Any, TypedDict
import logging
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from pydantic import ValidationError

from src.LLM.ollama import generatedStatus, generatePromptToCreateImage, \
  refineAndEstructuredPrompt

class State(TypedDict):
  idea: str
  prompt: str
  status: str

class GraphProcessor:
  def __init__(self):
    self.memory = MemorySaver()
    self.graph_builder = StateGraph(State)
    self._setupGraph()

  async def createInitialIdea(self, state: State) -> Dict[str, str]:
    try:
      prompt_step_one = await generatedStatus(state['idea'])
      data = orjson.loads(prompt_step_one)

      return {"prompt": data['prompt'], "status": data['status']}
    except orjson.JSONDecodeError as e:
      logging.error(f"Error decoding JSON: {str(e)}")
      raise
    except ValueError as e:
      logging.error(f"Validation error: {str(e)}")
      raise
    except Exception as e:
      logging.error(f"Unexpected error in createInitialIdea: {str(e)}")
      raise

  async def generateIdea(self, state: State) -> Dict[str, Any]:
    try:
      response = await generatePromptToCreateImage(state['prompt'])
      return {"prompt": response}
    except Exception as e:
      logging.error(f"Error in generateIdea: {str(e)}")
      raise

  async def refineIdea(self, state: State) -> Dict[str, Any] | str:
    try:
      response = await refineAndEstructuredPrompt(state['prompt'])
      return {"prompt": response.model_dump()}
    except ValidationError as e:
      logging.error(f"Validation error in refineIdea {str(e)}")
      return {"prompt": "Error"}
    except Exception as e:
      logging.error(f"Error in refineIdea: {str(e)}")
      return {"prompt": "Error"}

  async def conditionNodeRefinement(self, state: State) -> Literal["createInitialIdea", END]:
    if state['prompt'] == "Error":
      logging.warning("Model failed to generate response, retrying...")
      return "createInitialIdea"
    logging.info("Model successfully generated response")
    return END

  def _setupGraph(self) -> None:
    # Add nodes
    self.graph_builder.add_node("createInitialIdea", self.createInitialIdea)
    self.graph_builder.add_node("generateIdea", self.generateIdea)
    self.graph_builder.add_node("refineIdea", self.refineIdea)

    # Add edges
    self.graph_builder.add_edge(START, "createInitialIdea")
    self.graph_builder.add_edge("createInitialIdea", "generateIdea")
    self.graph_builder.add_edge("generateIdea", "refineIdea")
    self.graph_builder.add_conditional_edges(
      "refineIdea",
      self.conditionNodeRefinement
    )

  def compile(self):
    return self.graph_builder.compile(checkpointer=self.memory)

# Initialize graph
graph_processor = GraphProcessor()
graph = graph_processor.compile()
