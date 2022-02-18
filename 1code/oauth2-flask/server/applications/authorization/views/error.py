from _imports_ import *

from marshmallow import ValidationError

from ..exceptions import error_messages

@main.app_errorhandler(400)
def BadRequest(e):

    if issubclass(e,ValidationError):
        return render_template(
            'error.html',
            http_code=400,
            error_code=1001,
            error_message=error_messages[1001]
        ), 400

    else:
        return render_template(
            'error.html',
            http_code=400,
            error_code=1002,
            error_message=error_messages[1002]
        ), 400