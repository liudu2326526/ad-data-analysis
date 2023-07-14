import pandas as pd
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from google.oauth2 import service_account
from googleapiclient.http import build_http
from googleapiclient import discovery
from pandas_gbq import gbq
from config.conf import conf
from util import date_util
from util import bigquery_util

# 设置服务帐号密钥文件的路径
SERVICE_ACCOUNT_KEY_FILE = conf['SERVICE_ACCOUNT_KEY_FILE']
SERVICE_ACCOUNT_KEY_CACHE = conf['SERVICE_ACCOUNT_KEY_CACHE']
GOOGLE_SERVICE_ACCOUNT_KEY_FILE = conf['GOOGLE_SERVICE_ACCOUNT_KEY_FILE']
CREDENTIALS = service_account.Credentials.from_service_account_file(
    GOOGLE_SERVICE_ACCOUNT_KEY_FILE)

accounts = conf['ACCOUNTS']

dimension_dic = [
  'DATE',
  'COUNTRY_NAME',
  # 'AD_UNIT_NAME',
  # 'AD_UNIT_ID',
  'AD_FORMAT_NAME',
  'AD_FORMAT_CODE'
]
metric_dic = [
  'AD_REQUESTS',
  'MATCHED_AD_REQUESTS',
  'IMPRESSIONS',
  'CLICKS',
  'ESTIMATED_EARNINGS',
]


def get_adsense_service(client_secrets, credential_cache):
  name = 'adsense'
  version = 'v2'
  flow = client.flow_from_clientsecrets(client_secrets,
                                        scope='https://www.googleapis.com/auth/adsense.readonly',
                                        message=tools.message_if_missing(
                                            client_secrets))
  storage = file.Storage(credential_cache)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage)
  http = credentials.authorize(http=build_http())

  return discovery.build(name, version, http=http)


def get_default_adsense_service():
  client_secrets = SERVICE_ACCOUNT_KEY_FILE
  credential_cache = SERVICE_ACCOUNT_KEY_CACHE
  return get_adsense_service(client_secrets, credential_cache)


def run_report(target_day=date_util.today()):
  year, month, day = date_util.get_year_month_day(target_day)
  service = get_default_adsense_service()

  result = service.accounts().reports().generate(
      account=accounts,
      metrics=metric_dic,
      dimensions=dimension_dic,
      # dateRange='LAST_7_DAYS',
      currencyCode='USD',
      # dateRange='CUSTOM',
      endDate_day=day,
      endDate_month=month,
      endDate_year=year,
      startDate_day=day,
      startDate_month=month,
      startDate_year=year,
      # startDate='2023-07-14',
      # endDate='2023-07-14'
      # dateRange = {
      #   'start_date':'2023-07-10',
      #   'end_date':'2023-07-11'
      # }

  ).execute()

  # for h in result['headers']:
  #   print(h)
  df = pd.DataFrame(columns=dimension_dic + metric_dic)

  for r in result['rows']:
    values = []
    for v in r['cells']:
      values.append(v['value'])
    df = df.append(pd.Series(values, index=df.columns), ignore_index=True)

  print(df)

  bigquery_util.execute_gbq_dml_sql("""
delete from `maximal-park-391912.data_import.adsense_data`
where DATE = '{date}'
  """.format(date=target_day))

  bigquery_util.df_to_bigquery(df, 'data_import.adsense_data')


# df.to_csv('adsense_output.csv', index=False)

# gbq.to_gbq(df, 'data_import.adsense_data', project_id='maximal-park-391912',
#            credentials=CREDENTIALS, if_exists='append')


if __name__ == '__main__':
  run_report()
