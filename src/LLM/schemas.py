from pydantic import BaseModel, Field


class PromptSchemaResponse(BaseModel):
    """Schema for generating prompts, negative prompts, seeds, and configuration parameters for image creation."""

    prompt: str = Field(
        description="""
          A **highly detailed** description of the image, including themes like nature, sunsets, and related elements.
          Be extremely specific about colors, lighting, textures, composition, and atmosphere.
          Example: 'A serene forest with tall, ancient trees, their bark covered in moss,
          and sunlight filtering through the dense canopy, creating a magical, golden-green ambiance.
        """,
        required=True
    )

    negative_prompt: str = Field(
        description="""
          A detailed description of what should NOT appear in the image. Never include people or animals.
          Example: 'No people, no animals, no buildings, no artificial objects, no vehicles.'
        """,
        default=""
    )

    seed: int = Field(
        description="A positive number used as the seed for generating the image. Ensures reproducibility.",
        default=-1
    )

    hr_checkpoint_name: str = Field(
        description="The name of the model (checkpoint) to be used for image generation.",
        default="artio_xlV1"
    )

    sampler_name: str = Field(
        escription="The name of the sampling method to be used for image generation.",
        default="DPM++ 2M"
    )