# coding=utf-8
import json
import sys

import requests
import pandas as pd
from six import string_types
from six.moves.urllib.parse import urlencode, urlunparse  # noqa
from util import date_util
from util import bigquery_util
from config.conf import conf
from retrying import retry

ACCESS_TOKEN = conf['TIKTOK_ACCESS_TOKEN']
PATH = "/open_api/v1.3/report/integrated/get/"

dimension_dic = [
  "stat_time_hour",
  "campaign_id"
]
metric_dic = [
  "impressions",
  "clicks",
  "reach",
  "conversion",
  "spend"
]
data_type = {
  "impressions": int,
  "clicks": int,
  "reach": int,
  "conversion": int,
  'spend': float,
}

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


def get(json_str):
  # type: (str) -> dict
  """
  Send GET request
  :param json_str: Args in JSON format
  :return: Response in JSON format
  """
  args = json.loads(json_str)
  query_string = urlencode(
      {k: v if isinstance(v, string_types) else json.dumps(v) for k, v in
       args.items()})
  url = build_url(PATH, query_string)
  headers = {
    "Access-Token": ACCESS_TOKEN,
  }
  rsp = requests.get(url, headers=headers)
  return rsp.json()



@retry(wait_fixed=60000, stop_max_attempt_number=3)
def run_report(target_day=date_util.today()):
  print("run {} data".format(target_day))
  metrics = json.dumps(metric_dic)
  data_level = "AUCTION_CAMPAIGN"
  end_date = target_day
  page_size = 200
  start_date = target_day
  advertiser_id = conf['TIKTOK_ADVERTISER_ID']
  service_type = "AUCTION"
  report_type = "BASIC"
  page = 1
  dimensions = json.dumps(dimension_dic)

  # Args in JSON format
  my_args = "{\"metrics\": %s, \"data_level\": \"%s\", \"end_date\": \"%s\",\"advertiser_id\": \"%s\", \"page_size\": \"%s\", \"start_date\": \"%s\", \"service_type\": \"%s\", \"report_type\": \"%s\", \"page\": \"%s\", \"dimensions\": %s}" % (
    metrics, data_level, end_date, advertiser_id, page_size,
    start_date, service_type,
    report_type, page, dimensions)

  df = pd.DataFrame(columns=dimension_dic + metric_dic)

  json_data = get(my_args)

  for i in json_data['data']['list']:
    values = []
    for d in dimension_dic:
      values.append(i['dimensions'][d])
    for m in metric_dic:
      values.append(i['metrics'][m])
    df = df.append(pd.Series(values, index=df.columns), ignore_index=True)

  for k in data_type:
    df[k] = df[k].astype(data_type[k])
  print(df)

  bigquery_util.execute_gbq_dml_sql("""
delete from `maximal-park-391912.data_import.tiktok_data_hourly`
where stat_time_hour like '{date}%'
  """.format(date=target_day))

  bigquery_util.df_to_bigquery(df, 'data_import.tiktok_data_hourly')


if __name__ == '__main__':
  args = sys.argv
  today = date_util.today()
  if len(args) > 1:
    for i in range(int(args[1])):
      run_report(date_util.someday_from_day(today, i))
  else:
    run_report()
