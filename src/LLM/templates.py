from langchain_core.prompts import ChatPromptTemplate

from settings.LLM.input_prompt import instructions_user_prompt
from settings.LLM.instructions_model_llm import instructions_system_model_llm
from settings.LLM.instructions_model_improve import instructions_system_model_improvements


prompt_template_to_improve = ChatPromptTemplate.from_messages(
    [("system", instructions_system_model_improvements),
    ("user", "{input}")]
)

prompt_template_to_llm = ChatPromptTemplate.from_messages(
    [("system", instructions_system_model_llm ),
    ("human", instructions_user_prompt )]
)