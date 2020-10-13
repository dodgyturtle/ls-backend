import settings.settings_errors as errors


def response_processing(error_code: int, data: str = None):
    api_response = {
        'code': error_code,
        'message': errors.DECODING_CODES.get(error_code, errors.TEXT_IF_NO_CODE),
        'data': data,
    }
    return api_response