import os

# check whitelist
def check_origin(url: str):
    return url in os.environ["WHITELIST"].split(",")
