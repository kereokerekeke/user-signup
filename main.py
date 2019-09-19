from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


def check_validity(type, string):

    error = False

    if (string != ''):
        if (' ' in string) or (3 > len(string) or len(string) > 21):
            error = True
        if type == 'Email' and ((string.count('@') != 1) or (string.count('.') != 1)):
            error = True
    elif type != 'Email':
        error = True
    
    if error:
        return type + ' not valid' 
    else:
        return ''


@app.route('/', methods=['GET', 'POST'])
def signup():
    
    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''
    username = ''
    email = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        
        username_error = check_validity('Username', username)
        password_error = check_validity('Password', password)
            
        if verify != password:
            verify_error = 'Passwords do not match'

        email_error = check_validity('Email', email)
        
        if not username_error and not password_error and not verify_error and not email_error:
            return redirect('/welcome?username={username}'.format(username=username))

    return render_template('signup.html',
                           title='Signup',
                           username_error=username_error,
                           email_error=email_error,
                           password_error=password_error,
                           verify_error=verify_error,
                           username=username,
                           email=email)


@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html',
                           username=username)
    

app.run()