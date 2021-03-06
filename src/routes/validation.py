from flask import request
from secrets import compare_digest

from src.errorsModule.errors_fun import error_response
from src.sqlalchemyModule.users import UsersDb


def valid_request_type(types):
    """Check if content type of flask response of an inner function is valid type.

    Args:
        types (tuple): a tuple that includes all acceptable content types
    """

    def inner(fun):
        def wrapper(*args, **kwargs):
            # extract the request content-type from a request
            try:
                request_content_type = request.headers['content-type'].split(";")[0]
            except:
                return error_response(409, "SYNTAX", "Missing request body", "Please include multipart/form-data body")
            if request_content_type not in types:
                return error_response(409, "SYNTAX", "Unacceptable content-type",
                                      "Please only use multipart/form-data content-type")
            return fun(*args, **kwargs)

        return wrapper

    return inner


def valid_user(username, password):
    """validate username and password and make sure they belong to the same user

    Args:
        username (str): the username to compare with password
        password (str): the password to compare with username

    Returns:
        True (boolean): if password matches the username's password in the db
    """
    try:
        user = UsersDb.query.filter_by(username=username).one()
        db_password = user.password
        if compare_digest(password, db_password):
            return True
        else:
            raise Exception("403", "UNAUTHORIZED",
                            "Wrong password or username.", "")
    except Exception as error:
        raise Exception("403", "UNAUTHORIZED",
                        "Wrong password or username.", error)


def valid_wtform(form):
    """Validates request fields with wtforms validations

    Args:
        form(class): wtform template
    """

    def inner(fun):
        def wrapper(*args, **kwargs):
            try:
                # wtforms
                new_form = form()
                # validate the wtform fields
                new_form.validate_on_submit()
                # make sure there are no errors
                errors = new_form.errors
                for field, error_messages in errors.items():
                    return error_response(409, "CONFLICT",
                                          error_messages[0].replace("Field", field).replace("This field",
                                                                                            field + " field"))
                return fun(*args, **kwargs)
            except Exception as error:
                return error_response(409, "SYNTAX", "Invalid form fields", error)

        return wrapper

    return inner


def password_match(main_password, confirm_password, message=None):
    """Takes main password and a password to compare it with, and raises an error if 
    the passwords are not matching.

    Args:
        main_password (str): the main password
        confirm_password (str): the confirmation password to compare
        message (str) optional: optional error message, defaults to password not matching

    Raises:
        Exception: passwords values are not matching
    """
    # default message if message is not set
    if not message:
        message = 'Passwords are not matching.'
    # check if passwords are not matching
    if not compare_digest(main_password, confirm_password):
        raise Exception("409", "CONFLICT", message, "")
