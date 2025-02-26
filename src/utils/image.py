import orjson
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import uuid
from pathlib import Path
import logging
from typing import List, Dict, Optional


from settings.config import ENV, OUTPUT_DIR


def requestStableDifusion(payload: Dict) ->  List[str]:
  """
  Genera imágenes usando Stable Diffusion API.

  Args:
      payload (Dict): Parámetros para la generación de imágenes

  Returns:
      List[str]: Lista de rutas de las imágenes generadas
  """
  try:
    payload_json = orjson.dumps(payload)
    response = requests.post(
      url=f"{ENV['BASE_URL']}/sdapi/v1/txt2img",
      data=payload_json
    ).json()

    paths = []
    for img_data in response['images']:
      path = OUTPUT_DIR / f'image_{uuid.uuid4()}.png'
      image = Image.open(io.BytesIO(base64.b64decode(img_data)))
      pnginfo = PngImagePlugin.PngInfo()
      pnginfo.add_text("parameters", str(response['info']))
      image.save(path, pnginfo=pnginfo)
      paths.append(str(path))
      logging.info(f"Imagen guardada en: {path}")
    return paths
  except Exception as e:
    logging.error(f"Error en requestStableDifusion: {str(e)}")
    raise

def createPayload(kwargs: Dict) -> Dict:
  """
  Crea el payload para la API de Stable Diffusion.

  Args:
      kwargs (Dict): Parámetros para actualizar el payload base

  Returns:
      Dict: Payload actualizado
  """
  try:
    path_template = Path('settings/template-payload.json')
    if not path_template.exists():
      raise FileNotFoundError(f"Template no encontrado en: {path_template}")

    base_config = orjson.loads(path_template.read_text())
    base_config.update({k: v for k, v in kwargs.items() if k in base_config})
    logging.debug(f"Payload creado: {base_config}")
    return base_config
  except Exception as e:
    logging.error(f"Error en createPayload: {str(e)}")
    raise

def getModels() -> str:
  """
  Obtiene la lista de modelos disponibles.

  Returns:
      str: Lista de modelos separados por comas
  """
  try:
    response = requests.get(
      f"{ENV['BASE_URL']}/sdapi/v1/sd-models",
      timeout=10
    ).json()
    models = [model['model_name'] for model in response]
    return ", ".join(models)
  except Exception as e:
    logging.error(f"Error obteniendo modelos: {str(e)}")
    raise

def getSamplingMethods() -> str:
  """
  Obtiene los métodos de sampling disponibles.

  Returns:
      str: Lista de métodos de sampling separados por comas
  """
  try:
    response = requests.get(
      f"{ENV['BASE_URL']}/sdapi/v1/samplers",
      timeout=10
    ).json()
    methods = [sampler['name'] for sampler in response]
    return ", ".join(methods)
  except Exception as e:
    logging.error(f"Error obteniendo métodos de sampling: {str(e)}")
    raise

