import sys

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
  DateRange,
  Dimension,
  Metric,
  RunReportRequest
)
from config.conf import conf
from util import date_util
from util import bigquery_util

dimension_dic = [
  'date',
  'country',
  'countryId',
  'adFormat',
  'adUnitName',
  'landingPagePlusQueryString'
]
metric_dic = [
  'publisherAdClicks',
  'publisherAdImpressions',
  'totalAdRevenue'
]

# 设置服务帐号密钥文件的路径
SERVICE_ACCOUNT_KEY_FILE = conf['GOOGLE_SERVICE_ACCOUNT_KEY_FILE']
CREDENTIALS = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY_FILE)
# 设置要访问的 GA4 属性 ID
PROPERTY_ID = conf['PROPERTY_ID']


def authenticate():
  """通过服务帐号身份验证"""
  credentials = service_account.Credentials.from_service_account_file(
      SERVICE_ACCOUNT_KEY_FILE,
      scopes=['https://www.googleapis.com/auth/analytics.readonly']
  )
  # 检查是否存在刷新令牌，如果有，则刷新令牌
  if credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())
  return credentials


def run_report(target_day=date_util.today()):
  print("run {} data".format(target_day))
  # 进行身份验证
  credentials = authenticate()

  # 创建 GA4 客户端
  client = BetaAnalyticsDataClient(credentials=credentials)
  print("已连接到 Google Analytics Data API")
  # 创建报告请求对象
  request = RunReportRequest(
      property=f"properties/{PROPERTY_ID}",
      dimensions=[Dimension(name=name) for name in dimension_dic],  # 按日期分组
      metrics=[Metric(name=name) for name in metric_dic],
      date_ranges=[DateRange(start_date=target_day, end_date=target_day)],
      limit=250000
  )

  # 包装请求并设置超时时间
  response = client.run_report(request)

  # print(response)
  rows = []
  # 处理响应数据
  df = pd.DataFrame(columns=dimension_dic + metric_dic)

  for row in response.rows:
    values = []
    for dimension in row.dimension_values:
      values.append(dimension.value)
    for metric in row.metric_values:
      values.append(metric.value)
    df = df.append(pd.Series(values, index=df.columns), ignore_index=True)

  print(df)

  bigquery_util.execute_gbq_dml_sql("""
delete from `maximal-park-391912.data_import.analytic_data_daily`
where DATE = '{date}'
  """.format(date=date_util.chuange_format(target_day)))

  bigquery_util.df_to_bigquery(df, 'data_import.analytic_data_daily')


if __name__ == '__main__':
  args = sys.argv
  today = date_util.today()
  if len(args) > 0:
    for i in range(int(args[0])):
      run_report(date_util.someday_from_day(today, i))
  else:
    run_report()
