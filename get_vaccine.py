import requests
import os

session = None
prefix = 'https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx'
city = ["", "", ""]
cityCode = 510000
product = 1


def parse_params(params):
    url_params = '?'
    for key, value in params.items():
        url_params = url_params + str(key) + '=' + str(value) + '&'
    return url_params[:-1]


def get(data):
    global session
    headers = {
        "Referer": "https://servicewechat.com/wx2c7f0f3c30d99445/91/page-frame.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI "
                      "MiniProgramEnv/Windows WindowsWechat",
        "content-type": "tex/plain; charset=utf-8",
    }
    if not session:
        session = requests.Session()
    url = prefix + parse_params(data)
    result = None
    response = session.get(url, headers=headers, timeout=2)
    if response.status_code == 200:
        result = response.json()
        return result
    return {}


def get_customer_list():
    data = {
        "act": "CustomerProduct",
        "id": 0,
        "lng": "106.46862",
        "lat": "26.55261"
    }
    result = get(data)
    return list(filter(lambda x: "莲湖区" in x["cname"], result["list"]))


def get_customer_product(customer_id):
    data = {
        "act": "CustomerProduct",
        "id": customer_id
    }
    product_list = get(data)["list"]
    result = list(filter(lambda x: "九价" in x["text"], product_list))
    return result["BtnLable"] != "暂未开始"


def get_customer_subscribe_date_all():
    for customer_item in customer_list:
        data = {
            "act": "GetCustSubscribeDateAll",
            "pid": product,
            "id": customer_item["id"],
            "month": "202112"
        }
        print(1)
        date_list = get(data)["list"]
        print("date", date_list)


if __name__ == '__main__':
    # customer_list = get_customer_list()
    # customer_product = get_customer_product()
    # get_customer_subscribe_date_all()
    query_hospital_param = {
        "act": "CustomerList",
        "city": ["", "", ""],
        "lng": "106.46862",
        "lat": "26.55261"
    }
    query_vaccine_param = {
        "act": "CustomerProduct",
        "id": 6701,
        "lng": "106.46862",
        "lat": "26.55261"
    }
    result = get(query_hospital_param)
    hospital_list = result.get("list")
    if hospital_list is not None:
        for hospital in hospital_list:
            query_vaccine_param["id"] = hospital.get("id")
            hospital_info = get(query_vaccine_param)
            hospital_name = hospital_info.get("cname")
            vaccine_list = hospital_info.get("list")
            if vaccine_list is not None:
                for vaccine in vaccine_list:
                    if "九价" in vaccine.get("text") and vaccine.get("enable") == True: 
                        cmd = "curl -d \'title={} 九价疫苗可预约&desp={}\' -X POST https://sctapi.ftqq.com/SCT155769TeFx6NcwGJFDxoU4zxOWNr96L.send".format(
                            hospital_name,
                            "快前往预约吧！"
                        )
                        os.system(cmd)
