from flask import Flask, render_template
from app import app
from app.forms import LoginForm
from appc import pundit
from flask-pundit import
from flask_pundit import verify_authorized
from appc import app, pundit

app = Flask(__name__)
pundit = FlaskPundit(app)
pundit.init_app(app)

blogs = [{title:"Blog Post 1", data: "Lorem ipsum "},{title: "Blog Post 2", data: "Lorem ipsum"}]

@app.route('/')
def index():
    return render_template('index.html', blogs)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
                return redirect(next_page)
            return redirect(url_for('home'))
    return render_template('login.html', title ='Login', form = form)

@app.route('/blog/<string: title>')
def blogpost():
    return render_template()

@app.route('/posts)
def index():
        all_posts = pundit.policy_scope(Post)
        return all_posts

app = Flask('blog_series')
pundit = FlaskPundit(app)

@app.route('/blogs/<id>')
def read_blog_post(id):
        blog = Post.get_by_id(id)
        if pundit.authorize(post):
                return blog
        return ForbiddenError, 403

@app.route('/posts/<id>')
@verify_authorized
def read_blog_post(id):
        blog_post = Post.get_by_id(id)
        if pundit.authorize(blog_post):
                return blog_post
        return ForbiddenError, 403

@app.route('/adminOptions')
def adminOptions():
    return render_template('adminOptions.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# @app.route('/firstEntry')
# def firstEntry():
#     return render_template('firstEntry.html')
#
# @app.route('/secondEntry')
# def secondEntry():
#     return render_template('secondEntry.html')
#
# @app.route('/thirdEntry')
# def thirdEntry():
#     return render_template('thirdEntry.html')
