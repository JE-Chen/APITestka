from je_api_testka import test_api_method

if __name__ == "__main__":
    import requests

    test_response = test_api_method("put", "http://httpbin.org/put", params={"task": "new task"})
    print(test_response.get("response_data").get("status_code"))
    print(test_response.get("response_data").get("text"))
    try:
        test_response = test_api_method("put", "dawdwadaw")
    except requests.exceptions.MissingSchema as error:
        print(repr(error))
    from je_api_testka import APITesterException

    try:
        test_response = test_api_method("http://httpbin.org/get", "put")
    except APITesterException as error:
        print(repr(error))
