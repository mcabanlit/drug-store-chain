import requests
# r = requests.post('http://127.0.0.1:5000/predict',
#                  json={
#                      "Store": 1111
#                  })



r = requests.post('https://drug-store-chain.herokuapp.com/predict', json={
                      "Store":1111,
                      "DayOfWeek":4,
                      "Date":"2014-07-10",
                      "Customers":410,
                      "Open":1,
                      "Promo":0,
                      "StateHoliday":"b",
                      "SchoolHoliday":1
                 })

print(r.text)