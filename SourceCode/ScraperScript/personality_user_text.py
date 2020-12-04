import requests
import json
from requests.auth import HTTPBasicAuth

url = "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13"
headers = {"Content-Type" : "text/plain;charset=utf-8", "Accept" : "application/json"}
api_key = HTTPBasicAuth('apikey', 'MjVNB2gksOOEQpnAiyboO3h4Ex1EQmkUdcGZh_DWMQ4E')

def get_data_for_user():	
	raw_data_file_ptr = open("web_chat_data.en", "r")
	count = 0
	user_count = 0
	base_line = ""

	dict_of_text = {}

	for line in raw_data_file_ptr.readlines():
		count += 1

		if count == 200:
			dict_of_text["user_{}".format(user_count)] = base_line

			req = requests.post(url, headers=headers, auth=api_key, data=base_line)
			with open("user_{}.json".format(user_count), "w") as out:
				res = json.dump(req.content, out, sort_keys=True, indent=4, separators=(',', ': '))

			user_count += 1
			count = 0
			base_line = ""


		base_line = base_line + line

	print(dict_of_text)

if __name__ == "__main__":
	get_data_for_user()



