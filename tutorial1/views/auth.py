from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    next_url = request.params.get('next')
    if not next_url:
        next_url = request.route_url('view_page', pagename='FrontPage')
    message = request.params.get('message', '')
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            user.loggedIn = True
            if user.role == "editor":
                next_url = request.route_url('editor_page')
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        app_category='login',
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )


@view_config(route_name='registerUser', renderer='../templates/registerUser.jinja2')
def registerUser(request):
    message = ''
    username = ''
    errors = []
    if 'form.submitted' in request.params:
        username = request.params['username']
        password1 = request.params['password1']
        password2 = request.params['password2']

        # Validation
        if len(username.strip()) == 0:
            errors.append('Username cannot be blank')
        if len(password1) == 0:
            errors.append('Password cannot be blank')
        if password1 != password2:
            errors.append('Passwords do not match')

        if not len(errors):
            # Add object to database
            new_user = User()
            new_user.name = username
            new_user.role = 'basic'
            new_user.set_password(password1)
            request.dbsession.add(new_user)
            try:
                request.dbsession.flush()
                headers = remember(request, new_user.id)
                return HTTPFound(location=request.route_url('view_wiki'), headers=headers)
            except IntegrityError:
                errors.append('Username already exists')

        message = 'Try Again'

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('registerUser'),
        username=username,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    request.user.loggedIn = False
    next_url = request.route_url('view_wiki')
    return HTTPFound(location=next_url, headers=headers)


#@forbidden_view_config()
#def forbidden_view(request):
#    next_url = request.route_url('login', _query={'next': request.url, 'message': 'You must be logged in to view that page'})
#    return HTTPFound(location=next_url)
