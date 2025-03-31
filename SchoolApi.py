import requests
import json

class SchoolApi:

    params = {
        "KEY": "bea2b7358e3945d6a13530831ea0fa23",
        "Type": "json",
    }

    schoolinfo = {}

    base_url = "https://open.neis.go.kr/hub/"
