from je_api_testka import test_api_post

test_response = test_api_post("http://httpbin.org/post", params={"task": "new task"})
print(test_response.get("response_data").get("status_code"))
print(test_response.get("response_data").get("status_code"))
