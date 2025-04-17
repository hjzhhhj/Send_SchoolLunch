import requests
import json
import os

class SchoolApi:
    params = {
        "KEY": os.getenv("NEIS_API_KEY"),
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
        if not data or not isinstance(data, list):
            return "급식 정보를 가져올 수 없습니다."

        try:
            meal_map = {
                "1": "<조식>",
                "2": "<중식>",
                "3": "<석식>"
            }

            result = ""
            characters = "1234567890./-*"

            for meal in data:
                meal_name = meal_map.get(meal.get("MMEAL_SC_CODE", ""), "")
                dish = meal.get("DDISH_NM", "").replace("<br/>", "\n")

                # 특수문자 제거
                for c in characters:
                    dish = dish.replace(c, "")

                if meal_name and dish:
                    result += f"{meal_name}\n{dish}\n\n"

            return result.strip() if result else "오늘은 급식이 없습니다."
        except Exception as e:
            print(f"Error: {e}")
            return "급식 정보 처리 중 오류가 발생했습니다."
