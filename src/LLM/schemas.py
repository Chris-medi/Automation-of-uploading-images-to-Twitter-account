from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class SamplerName(str, Enum):
  DPM = "DPM++ 2M"
  EULER = "Euler a"
  DDIM = "DDIM"
  UNIPC = "UniPC"

class ModelCheckpoint(str, Enum):
  ARTIO = "artio_xlV1"
  STABLE = "stable_diffusion_2"
  SDXL = "sd_xl_base_1.0"

class PromptSchemaResponse(BaseModel):
  """Schema for generating prompts, negative prompts, seeds, and configuration parameters for image creation."""

  prompt: str = Field(
    description="A highly detailed description of the image",
    min_length=10,
    examples=["A serene forest with tall, ancient trees, their bark covered in moss"]
  )

  negative_prompt: Optional[str] = Field(
    default="",
    description="Elements to exclude from the image",
    examples=["No people, no animals, no car"]
  )

  seed: Optional[int] = Field(
    default=-1,
    description="Seed for reproducible image generation",
    ge=-1,  # greater than or equal to -1
    le=2**32 - 1  # maximum 32-bit integer
  )

  hr_checkpoint_name: Optional[str] = Field(
    default=ModelCheckpoint.ARTIO,
    description="Model checkpoint for image generation"
  )

  sampler_name: Optional[str] = Field(
    default=SamplerName.DPM,
    description="Sampling method for image generation"
  )

  @field_validator('prompt')
  def validatePromptContent(cls, v: str) -> str:
    if len(v.split()) < 3:
      raise ValueError("Prompt must contain at least 3 words")
    return v.strip()

  class Config:
    use_enum_values = True
    json_schema_extra = {
      "examples": [
        {
          "prompt": "A serene forest with tall, ancient trees",
          "negative_prompt": "No people, no , no car",
          "seed": 42,
          "hr_checkpoint_name": "artio_xlV1",
          "sampler_name": "DPM++ 2M"
        }
      ]
    }