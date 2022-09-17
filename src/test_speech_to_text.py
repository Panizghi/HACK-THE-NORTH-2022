import os
import requests

AAI_KEY = os.getenv("AAI_KEY")

print(AAI_KEY)


resp = requests.post("https://api.assemblyai.com/v2/", 
        headers={"content-type": "application/json", "authorization": AAI_KEY})

print(resp.text)
