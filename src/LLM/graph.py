from langgraph.checkpoint.memory import MemorySaver

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.types import Command, interrupt

from langchain_ollama import ChatOllama


class MessagesState(TypedDict):
  messages: Annotated[list, add_messages]

memory = MemorySaver()


llm = ChatOllama(
  model="llama3.2:3b",
  base_url="192.168.1.9:11434",
  # other params ...
)

async def chatbot(state: MessagesState):
    response = await model.ainvoke(state["messages"])
    return {"messages": response}

graph_builder = StateGraph(MessagesState)

graph_builder.add_node("chatbot", chatbot)

#
graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=memory)


# # Async invocation:
# output = await app.ainvoke({"messages": input_messages}, config)
# output["messages"][-1].pretty_print()
