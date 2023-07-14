from google.cloud import bigquery
from config.conf import conf
from google.oauth2 import service_account
from pandas_gbq import gbq

PROJECT_ID = 'mobiuspace-215609'
CREDENTIALS = service_account.Credentials.from_service_account_file(
    conf['GOOGLE_SERVICE_ACCOUNT_KEY_FILE'])
project_id = 'maximal-park-391912'


def execute_gbq_dml_sql(sql):
  print(sql)
  bg_client = bigquery.Client(project=project_id,
                              credentials=CREDENTIALS)
  delete_query = bg_client.query(sql)
  delete_query.result()
  print("Affected {} records.".format(delete_query.num_dml_affected_rows))
  return delete_query.num_dml_affected_rows


def df_to_bigquery(df, table_name):
  gbq.to_gbq(df, table_name, project_id=project_id,
             credentials=CREDENTIALS, if_exists='append')
