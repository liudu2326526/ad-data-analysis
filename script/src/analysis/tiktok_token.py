# coding=utf-8
import json
import requests

from six import string_types
from six.moves.urllib.parse import urlencode, urlunparse  # noqa

PATH = "/open_api/v1.3/oauth2/access_token/"


def build_url(path, query=""):
  # type: (str, str) -> str
  """
  Build request URL
  :param path: Request path
  :param query: Querystring
  :return: Request URL
  """
  scheme, netloc = "https", "business-api.tiktok.com"
  return urlunparse((scheme, netloc, path, "", query, ""))


def post(json_str):
  # type: (str) -> dict
  """
  Send POST request
  :param json_str: Args in JSON format
  :return: Response in JSON format
  """
  url = build_url(PATH)
  args = json.loads(json_str)
  headers = {
    "Content-Type": "application/json",
  }
  rsp = requests.post(url, headers=headers, json=args)
  return rsp.json()


# https://hpip.work/?home=1&more=1&auth_code=e5c5eda4ace14b9516f9dd2a492aa654df49107b&code=e5c5eda4ace14b9516f9dd2a492aa654df49107b&state=your_custom_params
# https://hpip.work/?home=1&more=1&auth_code=56747b23684d0132ce02152d92ac5dc83d0465c9&code=56747b23684d0132ce02152d92ac5dc83d0465c9&state=your_custom_params
if __name__ == '__main__':
  secret = '2482f36a8ea9d2f6f9196aa101a31ce836194be2'
  app_id = '7258183707175944194'
  # auth_code = '56747b23684d0132ce02152d92ac5dc83d0465c9' # old
  auth_code = 'e5c5eda4ace14b9516f9dd2a492aa654df49107b'

  # Args in JSON format
  my_args = "{\"secret\": \"%s\", \"app_id\": \"%s\", \"auth_code\": \"%s\"}" % (
    secret, app_id, auth_code)
  print(post(my_args))

# {'code': 0, 'message': 'OK', 'request_id': '2023080106430007347AB52060FF0681E1',
#  'data': {'access_token': '09563f450a6019d0140108fcc2f009767c35191f',
#           'advertiser_ids': ['7226633881561153538', '7237023178701258753'],
#           'scope': [4]}}

{'code': 0, 'message': 'OK', 'request_id': '20230808063530705ABD79629E14338D0A',
 'data': {'access_token': '1646256b9fa0524c9ff65084369439e7b8e89f70',
          'advertiser_ids': ['7260799450258391042', '7260799488309133313',
                             '7260799498249682945'], 'scope': [4]}}
