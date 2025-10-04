import http.client
import json

def send_message(to_number: str, text: str):
    conn = http.client.HTTPSConnection("api.infobip.com")
    payload = json.dumps({
        "messages": [
            {
                "destinations": [{"to":to_number}],
                "from": "447491163443",
                "text": text
            }
        ]
    })
    headers = {
        'Authorization': 'App 9022ecdb26ad778ae5e99b5ef7a07a10-518e637c-2739-480c-bbb4-3be8e63a96ba',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))