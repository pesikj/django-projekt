import requests
response = requests.get("http://localhost:8000/api/companies/")
print(response.text)