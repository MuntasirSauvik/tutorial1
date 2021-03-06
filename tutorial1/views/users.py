from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import transaction

from .. import models


@view_config(route_name='user_list', renderer='../templates/users/userList.jinja2')
def user_list(request):
    res = request.dbsession.query(models.User).all()
    return dict(res=res)


@view_config(route_name='user_add', renderer='../templates/users/userAdd.jinja2')
def user_add(request):
    message = ''
    username = ''
    role = ''
    errors = []
    if 'form.submitted' in request.params:
        username = request.params['username']
        password1 = request.params['password1']
        password2 = request.params['password2']
        role = request.params['role']

        # Validation
        if len(role.strip()) == 0:
            errors.append('Username cannot be blank')
        if len(username.strip()) == 0:
            errors.append('Username cannot be blank')
        if len(password1) == 0:
            errors.append('Password cannot be blank')
        if password1 != password2:
            errors.append('Passwords do not match')
        if role != "basic" and role != "editor":
            errors.append('Roles can either be basic or editor')

        if not len(errors):
            # Add object to database
            new_user = models.User()
            new_user.name = username
            new_user.role = role
            new_user.loggedIn = False
            new_user.set_password(password1)
            request.dbsession.add(new_user)
            try:
                request.dbsession.flush()
                return HTTPFound(location=request.route_url('editor_page'))
            except IntegrityError:
                errors.append('Username already exists')
                request.dbsession.rollback()

        message = 'Try Again'

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('user_add'),
        username=username,
        )


@view_config(route_name='user_modify', renderer='../templates/users/userModify.jinja2')
def user_modify(request):
    message = ''
    username = ''
    role = ''
    errors = []
    res = request.dbsession.query(models.User).get(request.matchdict["userId"])

    if 'form.submitted' in request.params:
        username = request.params['username']
        password1 = request.params['password1']
        password2 = request.params['password2']
        role = request.params['role']

        # Validation
        if len(role.strip()) == 0 and len(username.strip()) == 0 and len(password1) == 0:
            errors.append('Nothing to update')
        if len(role.strip()) != 0 and role not in ["basic", "editor"]:
            errors.append('Roles can either be basic or editor')
        if len(role.strip()) != 0 and role in ["basic", "editor"] and res is request.user:
            errors.append('You cannot change your own role')
        if len(password1) != 0 and password1 != password2:
            errors.append('Passwords do not match')

        # Update Information
        if not len(errors):
            # Update role
            if len(role.strip()) != 0:
                res.role = role
            if len(username.strip()) != 0:
                res.name = username
            if len(password1) != 0 and password1 == password2:
                res.set_password(password1)

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('user_modify', userId=request.matchdict["userId"]),
        username=username,
        res=res,
    )


@view_config(route_name='user_remove', renderer='../templates/users/userRemove.jinja2')
def user_remove(request):
    message = ''
    username = ''
    errors = []

    if 'form.submitted' in request.params:
        username = request.params['username']
        password1 = request.params['password1']

        # Validation
        if len(username.strip()) == 0 and len(password1) == 0:
            errors.append('Nothing entered')
        elif len(password1) != 0 and not request.user.check_password(password1):
            errors.append('You entered a wrong Password')
        else:
            try:
                user = request.dbsession.query(models.User.name).filter_by(name=username).one()
                print(user)
                user1 = request.dbsession.query(models.User).filter_by(name=username).one()
                request.dbsession.delete(user1)
            except NoResultFound:
                errors.append('Username does not exist')

        messages = '\n'.join(errors)

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('user_remove'),
        username=username,
    )
