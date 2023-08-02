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
  'TIKTOK_ACCESS_TOKEN': '09563f450a6019d0140108fcc2f009767c35191f',
  'TIKTOK_ADVERTISER_ID': 7237023178701258753,

}
