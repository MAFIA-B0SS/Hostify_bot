import requests
import json
from requests.structures import CaseInsensitiveDict

def DisableWorkFlow(workflow_id):
    import requests
    from requests.structures import CaseInsensitiveDict

    url = "https://api.github.com/repos/mubarak823/hostify_bot/actions/runs/"+str(workflow_id)+"/cancel"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.github+json"
    headers["Authorization"] = "Bearer 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"
    headers["Content-Type"] = "application/json"


    resp = requests.post(url, headers=headers)

    print(resp.status_code)
def DeleteWorkFlow(workflow_id):
    import requests
    from requests.structures import CaseInsensitiveDict

    url = "https://api.github.com/repos/mubarak823/hostify_bot/actions/runs/"+str(workflow_id)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/vnd.github+json"
    headers["Authorization"] = "Bearer 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"


    resp = requests.delete(url, headers=headers)

    print(resp.status_code)


url = "https://api.github.com/repos/mubarak823/Hostify_bot/actions/runs"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/vnd.github+json"
headers["Authorization"] = "Bearer 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"


resp = requests.get(url, headers=headers)
json_resp = json.loads(resp.text)


for x in range(0,len(json_resp['workflow_runs'])):
    workflow_id = json_resp['workflow_runs'][x]['id']
    print("disapling: "+str(workflow_id))
    DisableWorkFlow(workflow_id)
    DeleteWorkFlow(workflow_id)

