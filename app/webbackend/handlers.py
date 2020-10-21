def errors_convert_dict_to_string(dict_errors: dict):
    for key in dict_errors:
        return(str(key) + ','.join(dict_errors.get(key)))
