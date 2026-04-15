from fastapi.responses import JSONResponse

def validation_error(errors):
    error_str = ""
    for error in errors:
        error_str = error_str + " " + error + "\n"
    response = JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": [
                        "body",
                    ],
                    "msg": f"The following errors were found:\n {error_str}",
                }
            ]
        },
    )
    return response