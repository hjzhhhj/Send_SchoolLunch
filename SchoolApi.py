import requests
import json

class SchoolApi:

    params = {
        "KEY": "bea2b7358e3945d6a13530831ea0fa23",
        "Type": "json",
    }

    schoolinfo = {}

    base_url = "https://open.neis.go.kr/hub/"

    def get_data(self):
        URL = SchoolApi.base_url + self.sub_url
        self.params.update(SchoolApi.params)
        self.params.update(SchoolApi.schoolinfo)
        response = requests.get(URL, params=self.params)

        try:
            j_response = json.loads(response.text)[self.sub_url]
            if j_response[0]["head"][0]["list_total_count"] == 1:
                return j_response[1]["row"][0]
            else:
                return j_response[1]["row"]
        except:
            print("찾는 데이터가 없습니다.")
            return response.text