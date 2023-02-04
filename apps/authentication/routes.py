

from flask import render_template, redirect, request, url_for,session
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import os
import boto3
from apps import login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

@login_manager.user_loader
def user_loader(id):
    if 'access_token' not in session:
        return None 
    user = Users()
    user.id = Users.get_user()
    print(user)
    return user

@blueprint.route('/')
def route_default():
     return render_template('home/index.html', segment='index')


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        client = boto3.client('cognito-idp',region_name='us-east-1')
        auth_response = client.initiate_auth(
            ClientId=os.getenv('COGNITO_APP_CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        if auth_response['AuthenticationResult']:
            session['username'] = username
            user = Users()
            user.id = Users.get_user()
            session['access_token'] = auth_response['AuthenticationResult']['AccessToken']
            login_user(user)
            return redirect(url_for('home_blueprint.index'))

    else:
        return render_template('accounts/login.html',
                               form=login_form)

@blueprint.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    create_account_form = CreateAccountForm(request.form)
    if 'SignUp' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        client = boto3.client('cognito-idp',region_name='us-east-1')
        response = client.sign_up(
        ClientId=os.getenv('COGNITO_APP_CLIENT_ID'),
        Username=username,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'name',
                'Value': username
            }
        ]
    )   
        if response['UserConfirmed'] == True:
                return render_template('accounts/SignUp.html',
                                    msg='User created successfully.',
                                    success=True,
                                    form=create_account_form)   
        else:
            session['username'] = username
            print(session)
            return redirect(url_for('authentication_blueprint.verify'))
    else:
        return render_template('accounts/SignUp.html', form=create_account_form)
@blueprint.route('/verify', methods=['GET', 'POST'])
def verify():
    create_account_form = CreateAccountForm(request.form)
    if 'verify' in request.form:
        code = request.form['code']
        client = boto3.client('cognito-idp',region_name='us-east-1')
        response = client.confirm_sign_up(
        ClientId=os.getenv('COGNITO_APP_CLIENT_ID'),
        Username=session['username'],
        ConfirmationCode=code
    )   
        if response:
                return render_template('accounts/SignUp.html',
                                    msg='User created successfully.',
                                    success=True,
                                    form=create_account_form)   
        else:
            return render_template('accounts/Verify.html', form=create_account_form)
    else:
        return render_template('accounts/Verify.html', form=create_account_form)
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
