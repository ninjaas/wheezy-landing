from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import file_handler
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.web.templates import WheezyTemplate

from models import EmailBase
from models import get_or_create
from wheezy.validation import Validator
from wheezy.validation.rules import email
from wheezy.validation.rules import required
from wheezy.core.descriptors import attribute
from wheezy.core.collections import attrdict
from wheezy.core.comp import u
from wheezy.validation.model import try_update_model


class HomePage(BaseHandler):

    def get(self):
        return self.render_response('wheezy.html')


class EmailCredential(object):
    email = u('')

email_validator = Validator({
    'email': [email, required],
})


class EmailPage(BaseHandler):

    def post(self):
        email_id = self.request.form.get("email")[0]
        credential = EmailCredential()
        credential.email = email_id
        if self.validate(credential, email_validator):
            room, created = get_or_create(EmailBase, email=email_id)
            if created:
                return self.json_response(
                    {'success': "You are successfully added. We will invite on the beta launch"})
            else:
                return self.json_response(
                    {'success': "We will invite on the beta launch", 'error': "You are already registered."})
        else:
            return self.json_response(
                {'error': "Wrong Email Address. Please Correct yourself."})


all_urls = [
    url('', HomePage, name='default'),
    url('email', EmailPage, name='email'),
    url('static/{path:any}',
        file_handler(root='static/'),
        name='static')
]

options = {}

# Template Engine
searchpath = ['']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[
        CoreExtension(),
        WidgetExtension(),
    ])
engine.global_vars.update({
    'h': html_escape
})
options.update({
    'render_template': WheezyTemplate(engine)
})

main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory
    ],
    options=options
)
