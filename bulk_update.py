import requests
import csv
import urllib
import json

# Insert API key & App Secret from the Branch dashboard, and the Link data key you want to change in each link **
branch_key = "YOUR_KEY"
branch_secret = "YOUR_SECRET"


# Insert filename for CSV containing links to update in first column, and values to add in second column **
ifile = open('branchlinks.csv', "r")

# Constants
branchendpoint = "https://api2.branch.io/v1/url?url="
reader = csv.reader(ifile, delimiter=',')

# Uncomment the next line if you want the script to skip the first line of the CSV
next(reader)

# Loop through CSV
for row in reader:

    # Retrieve link data for link being updated
    url = urllib.quote_plus(row[0])
    getrequest = branchendpoint + url + "&branch_key=" + branch_key
    linkdata = requests.get(getrequest)
    jsonData = json.loads(linkdata.text)

    if linkdata.status_code != 200:
        print('Failed: {}'.format( getrequest))
        continue

    # Set credentials for update API
    jsonData["branch_key"] = branch_key
    jsonData["branch_secret"] = branch_secret

    for key_to_update in jsonData.get("data", "no_data"):
        # Update specified data key
        if key_to_update == "utm_campaign":
            # print jsonData["data"]["utm_campaign"]
            jsonData["data"]["~campaign"] = jsonData["data"]["utm_campaign"]
            # print jsonData["data"]["~campaign"]
            del jsonData["data"]["utm_campaign"]

        if key_to_update == "utm_source":
            jsonData["data"]["~channel"] = jsonData["data"]["utm_source"]
            del jsonData["data"]["utm_source"]

        if key_to_update == "utm_medium":
            jsonData["data"]["~feature"] = jsonData["data"]["utm_medium"]
            del jsonData["data"]["utm_medium"]

    if jsonData.get('type', None) is not None:
        del jsonData['type']
    if jsonData.get('alias', None):
        del jsonData['alias']
    payload = json.dumps(jsonData)
    print("\n \n payload")
    print(payload)
    putrequest = branchendpoint + url

    print(putrequest)
    r = requests.put(putrequest, json=jsonData)
    print("\n \n")
    print(r.url)
    print(r)
    # print

ifile.close()
