import requests
import json

r = requests.get('http://www.google.com/trends/fetchComponent?hl=en-US&q=apple&cid=TIMESERIES_GRAPH_0&export=3&date=today%203-m')

print r.text
#response = json.loads(text)

#print response