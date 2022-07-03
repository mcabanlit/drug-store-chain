import requests
r = requests.post('http://127.0.0.1:5000/predict',
                 json={
                     "Store": 1111
                 })


print(r.text)