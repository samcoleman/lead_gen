
res = {"result": {
      "emails":[

      ],
      "facebook":[
        "http:\/\/www.facebook.com\/TheOGLashesByAllie"
      ],
      "instagram":[
        "http:\/\/www.instagram.com\/lashesbyallie"
      ],
      "twitter":[

      ],
      "linkedin":[

      ],
      "keywords":{
        "http:\/\/www.lashesbyallie.co.uk":{
          "eyelash":[
            {
              "count":2
            }
          ],
          "lash":[
            {
              "count":51
            }
          ],
          "classic":[
            {
              "count":1
            }
          ],
          "volume":[
            {
              "count":5
            }
          ],
          "russian":[
            {
              "count":1
            }
          ]
        }
      },
      "prices":{
        "http:\/\/www.lashesbyallie.co.uk":{
          "count":10
        }
      },
      "pages":0
    }
}

result = res["result"]

for link in result['keywords']:
    for key in result['keywords'][link]:
        print(result['keywords'][link][key][0]["count"])
