# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     create_account_form = CreateAccountForm(request.form)
#     if 'register' in request.form:

#         username = request.form['username']
#         email = request.form['email']

#         # Check usename exists
#         user = Users.query.filter_by(username=username).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Username already registered',
#                                    success=False,
#                                    form=create_account_form)

#         # Check email exists
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Email already registered',
#                                    success=False,
#                                    form=create_account_form)

#         # else we can create the user
#         user = Users(**request.form)
#         db.session.add(user)
#         db.session.commit()
        
#         # Delete user from session
#         logout_user()        

#         return render_template('accounts/register.html',
#                                msg='User created successfully.',
#                                success=True,
#                                form=create_account_form)

#     else:
#         return render_template('accounts/register.html', form=create_account_form)
# @blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm(request.form)
#     if 'login' in request.form:

#         # read form data
#         username = request.form['username']
#         password = request.form['password']

#         # Locate user
#         user = Users.query.filter_by(username=username).first()

#         # Check the password
#         if user and verify_pass(password, user.password):

#             login_user(user)
#             return redirect(url_for('authentication_blueprint.route_default'))

#         # Something (user or pass) is not ok
#         return render_template('accounts/login.html',
#                                msg='Wrong user or password',
#                                form=login_form)

#     if not current_user.is_authenticated:
#         return render_template('accounts/login.html',
#                                form=login_form)
#     return redirect(url_for('home_blueprint.index'))
# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = Users()
#     return user if user else None
