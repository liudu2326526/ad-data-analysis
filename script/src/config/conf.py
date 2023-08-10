import os

current_dir = os.path.split(os.path.realpath(__file__))[0]

conf = {
  # google
  'GOOGLE_SERVICE_ACCOUNT_KEY_FILE': current_dir + '/service_account.json',
  # analytic
  'PROPERTY_ID': '354562983',
  # adsense
  'SERVICE_ACCOUNT_KEY_FILE': current_dir + '/client_secret_installed.json',
  'SERVICE_ACCOUNT_KEY_CACHE': current_dir + '/credential_cache.json',
  'ACCOUNTS': 'accounts/pub-6659704105417760',
  'TIKTOK_ACCESS_TOKEN': '1646256b9fa0524c9ff65084369439e7b8e89f70',
  'TIKTOK_ADVERTISER_ID': ['7260799450258391042', '7260799488309133313',
                           '7260799498249682945'],

}
