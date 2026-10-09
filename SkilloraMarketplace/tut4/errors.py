from flask import jsonify

def problem(type_, title, status, detail, errors=None, headers=None):
    body = {"type": type_, "title": title, "status": status, "detail": detail}
    if errors is not None:
        body["errors"] = errors
    response = jsonify(body)
    response.status_code = status
    response.headers["Content-Type"] = "application/problem+json; charset=utf-8"
    if headers:
        for k, v in headers.items():
            response.headers[k] = v
    return response
