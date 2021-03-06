import datetime
import sys

import requests
from requests.structures import CaseInsensitiveDict

from je_api_testka.requests_wrapper.requests_http_method_wrapper import api_tester_method
from je_api_testka.utils.assert_result.result_check import check_result
from je_api_testka.utils.exception.exception_tag import delete_error_message
from je_api_testka.utils.exception.exception_tag import get_data_error_message
from je_api_testka.utils.exception.exception_tag import get_error_message
from je_api_testka.utils.exception.exception_tag import head_error_message
from je_api_testka.utils.exception.exception_tag import options_error_message
from je_api_testka.utils.exception.exception_tag import patch_error_message
from je_api_testka.utils.exception.exception_tag import post_error_message
from je_api_testka.utils.exception.exception_tag import put_error_message
from je_api_testka.utils.exception.exception_tag import session_error_message
from je_api_testka.utils.exception.exceptions import APITesterExecuteException
from je_api_testka.utils.exception.exceptions import APITesterGetDataException
from je_api_testka.utils.get_data_strcture.get_api_data import get_api_response_data
from je_api_testka.utils.test_record.test_record_class import test_record_instance

exception_message_dict = {
    "get": get_error_message,
    "put": put_error_message,
    "delete": delete_error_message,
    "post": post_error_message,
    "head": head_error_message,
    "options": options_error_message,
    "patch": patch_error_message,
    "session_get": session_error_message,
    "session_put": session_error_message,
    "session_patch": session_error_message,
    "session_post": session_error_message,
    "session_head": session_error_message,
    "session_delete": session_error_message,
    "session_options": session_error_message,

}


def get_response(response: requests.Response,
                 start_time: [str, float, int],
                 end_time: [str, float, int]) -> dict:
    """
    use requests response to create data dict
    :param response: requests response
    :param start_time: test start time
    :param end_time: test end time
    :return: data dict include [status_code, text, content, headers, history, encoding, cookies,
    elapsed, request_time_sec, request_method, request_url, request_body, start_time, end_time]
    """
    try:
        return get_api_response_data(response, start_time, end_time)
    except APITesterGetDataException:
        raise APITesterGetDataException(get_data_error_message)


def test_api_method(http_method: str, test_url: str,
                    soap: bool = False, record_request_info: bool = True,
                    clean_record: bool = False, result_check_dict: dict = None, **kwargs) \
        -> (requests.Response, dict):
    """
    set requests http_method url headers and record response and record report
    :param http_method:
    :param test_url:
    :param soap:
    :param record_request_info:
    :param clean_record:
    :param result_check_dict:
    :param kwargs:
    :return:
    """
    try:
        try:
            start_time = datetime.datetime.now()
            if soap is False:
                response = api_tester_method(http_method, test_url=test_url, **kwargs)
            else:
                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/soap+xml"
                return test_api_method(http_method, test_url=test_url, headers=headers, **kwargs)
            end_time = datetime.datetime.now()
            response_data = get_response(response, start_time, end_time)
            if clean_record:
                test_record_instance.clean_record()
            if result_check_dict is None:
                if record_request_info:
                    test_record_instance.test_record_list.append(response_data)
                return {"response": response, "response_data": response_data}
            else:
                check_result(response_data, result_check_dict)
                if record_request_info:
                    test_record_instance.test_record_list.append(response_data)
                return {"response": response, "response_data": response_data}
        except APITesterExecuteException as error:
            raise repr(error)
    except Exception as error:
        print(repr(error), file=sys.stderr)
        test_record_instance.error_record_list.append([
            {
                "http_method": http_method,
                "test_url": test_url,
                "soap": soap,
                "record_request_info": record_request_info,
                "clean_record": clean_record,
                "result_check_dict": result_check_dict
            },
            repr(error)]
        )
