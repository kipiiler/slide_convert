from dotenv import load_dotenv
import requests
import os

load_dotenv()
token = os.getenv('TOKEN')
# print(f"Token: {token}")



# url='https://mineru.net/api/v4/extract/task'
# header = {
#     'Content-Type':'application/json',
#     "Authorization":f"Bearer {token}"
# }
# data = {
#     'url':'https://courses.cs.washington.edu/courses/cse484/25sp/slides/cse484-lecture1-25sp.pdf',
#     'is_ocr':True,
#     'enable_formula': True,
#     'enable_table': True,
#     'language':'en',
# }

# res = requests.post(url,headers=header,json=data)
# print(res.status_code)
# print(res.json())
# print(res.json()["data"])

# id = "c0bf0f3a-0fa8-437d-9693-8ffc2902a44c"

# url = f'https://mineru.net/api/v4/extract/task/{id}'
# header = {
#     'Content-Type':'application/json',
#     "Authorization":f"Bearer {token}"
# }

# res = requests.get(url,headers=header)
# print(res.status_code)
# print(res.json())
# print(res.json()["data"])
