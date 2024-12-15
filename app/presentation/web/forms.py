from scaffold.web.forms import BaseForm
from wtforms import EmailField, validators


class SignUpForm(BaseForm):
    email = EmailField("Email address", [validators.InputRequired()])
