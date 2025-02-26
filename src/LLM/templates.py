from langchain_core.prompts import ChatPromptTemplate

from settings.LLM.input_prompt import instructions_user_prompt
from settings.LLM.instructions_model_llm import instructions_system_model_llm
from settings.LLM.instructions_model_improve import instructions_system_model_improvements


class PromptTemplates:
  @staticmethod
  def createTemplate(messages: list[tuple[str, str]]) -> ChatPromptTemplate:
    try:
      return ChatPromptTemplate.from_messages(messages)
    except Exception as e:
      raise ValueError(f"Failed to create template: {str(e)}")

  @classmethod
  def getImprovementTemplate(cls) -> ChatPromptTemplate:
    messages = [
      ("system", instructions_system_model_improvements),
      ("user", "{input}")
    ]
    return cls.createTemplate(messages)

  @classmethod
  def getLlmTemplate(cls) -> ChatPromptTemplate:
    messages = [
      ("system", instructions_system_model_llm),
      ("human", instructions_user_prompt)
    ]
    return cls.createTemplate(messages)

# Initialize templates
prompt_template_to_improve = PromptTemplates.getImprovementTemplate()
prompt_template_to_llm = PromptTemplates.getLlmTemplate()