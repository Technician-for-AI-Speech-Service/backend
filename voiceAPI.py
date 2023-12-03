import urllib3
import json
import base64

def voiceAPI():
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "57536e54-f9a7-4f44-9a3a-998b3692fba2"
    audioFilePath = "./hello.wav"
    languageCode = "korean"
    
    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()
    
    requestJson = {    
    "argument": {
        "language_code": languageCode,
        "audio": audioContents
    }
    }

    # REST API
    http = urllib3.PoolManager()
    response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
    body=json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    # print(str(response.data,"utf-8"))
    data = json.loads(response.data.decode("utf-8", errors='ignore'))    
    text_data = data['return_object']['recognized']

    return text_data