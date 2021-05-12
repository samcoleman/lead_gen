import requests
import python

api_file = open("API_KEY.txt", "r")

api_key = api_file.read()

api_file.close()

home = "skipton"

work = "padiham"

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"

r = requests.get(url + "&origins=" + home + "&destinations=" + work + "&key=" + api_key)

print(r.json())

time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
sec = r.json()["rows"][0]["elements"][0]["duration"]["value"]

print("\n Time is", time)