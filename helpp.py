import requests


def getUnUsedGroupNum():
    url = "http://welcome.444danbao.com/api/dbgroupnums?key=huionedb"

    try:
        response = requests.get(url)
        data = response.json()
        return data['data']
    except Exception as e:
        pass

    return []
