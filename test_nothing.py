import requests

response= requests.get("https://api.covid19india.org/data.json").json()
# print(response.json()['statewise'])
states=['kerala','goa']
result=[]
for data in response['statewise']:
    result+=[data for i in states if(data['state']==i.title())]
    # print('#',data['state'],'  sdfs  ',states)
print(result)    