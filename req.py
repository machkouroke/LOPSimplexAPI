import requests
import yaml

with open("test.yaml", "r") as stream:
    data = stream.read()
# print(data)
y = requests.get('http://127.0.0.1:5000/voir')
x = requests.post('http://127.0.0.1:5000/test', data={'script': data, 'e': 'rt'})
# z = requests.request('post','http://127.0.0.1:5000/test', {'test':data,'e':'rt'})
print(x.text)
