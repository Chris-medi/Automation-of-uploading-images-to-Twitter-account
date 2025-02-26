import orjson
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import uuid
from pathlib import Path

from settings.config import ENV


def requestStableDifusion(payload: dict):
  payload_json = orjson.dumps(payload)
  response = requests.post(url=f"{ENV['BASE_URL']}/sdapi/v1/txt2img", data=payload_json).json()
  paths = []
  for i in response['images']:
    path = f'output_images/image_{str(uuid.uuid4())}.png'
    image = Image.open(io.BytesIO(base64.b64decode(i)))
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", str(response['info']))
    image.save(f'{path}', pnginfo=pnginfo)
    paths.append(path)
  return paths

def createPayload(kwargs: dict) -> dict:
  path_template_base = Path('settings/template-payload.json')
  json = orjson.loads(path_template_base.read_text())
  json.update({k: v for k, v in kwargs.items() if k in json})
  print(json)
  return json

def getModels() -> list[dict]:
  response = requests.get(f"{ENV['BASE_URL']}/sdapi/v1/sd-models").json()
  models = list(map(lambda x: x['model_name'],response))
  return ", ".join(models)

def getSamplingMethods() -> list[dict]:
  response = requests.get(f"{ENV['BASE_URL']}/sdapi/v1/samplers").json()
  sampling_methods = list(map(lambda x: x['name'],response))
  return ", ".join(sampling_methods)

