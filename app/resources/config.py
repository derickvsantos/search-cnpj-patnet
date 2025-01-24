import os

URL = os.getenv("URL")
USER = os.getenv("USER")
PWD = os.getenv("PWD")
TOKEN = ""
TIMEOUT = 15
HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}