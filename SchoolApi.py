import requests
import json

class SchoolApi:
    params = {
        "KEY": "-",
        "Type": "json",
    }

    schoolinfo = {}
    base_url = "https://open.neis.go.kr/hub/"

    def __init__(self, sub_url, params={}):
        self.sub_url = sub_url
        self.params = params

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
        
    def get_school_info(self):
        data = self.get_data()

        SchoolApi.schoolinfo = {
            "ATPT_OFCDC_SC_CODE": data["ATPT_OFCDC_SC_CODE"],
            "SD_SCHUL_CODE": data["SD_SCHUL_CODE"]
        }

    # 급식 정보를 가져오는 메서드
    def meal(self):
        data = self.get_data()
        if not data:
            return "급식 정보를 가져올 수 없습니다."
        try:
            string = "<조식>\n"+data[0]["DDISH_NM"].replace("<br/>", "\n")+"\n\n"
            string+= "<중식>\n"+data[1]["DDISH_NM"].replace("<br/>", "\n")+"\n\n"
            string += "<석식>\n" + data[2]["DDISH_NM"].replace("<br/>", "\n")
            characters = "1234567890./-*"
            for x in range(len(characters)):
                string = string.replace(characters[x],"")
            return string
        except Exception as e:
            print(f"Error: {e}")
            return "급식 정보 처리 중 오류가 발생했습니다."


