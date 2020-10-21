from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.security import (
    remember,
    forget,
    )
from .. import models


@view_config(route_name='user_list', renderer='../templates/users/userList.jinja2')
def user_list(request):
    return {}


@view_config(route_name='user_add', renderer='../templates/users/userAdd.jinja2')
def user_add(request):
    return {}


@view_config(route_name='user_modify', renderer='../templates/users/userModify.jinja2')
def user_modify(request):
    return {}


@view_config(route_name='user_remove', renderer='../templates/users/userRemove.jinja2')
def user_remove(request):
    return {}
