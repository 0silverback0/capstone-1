from flask import Flask, render_template, redirect, session, g, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Artist, User, Post
from forms import AddArtist, Signup, Login, PostForm, Edit
from api import get_artist_id, get_artist_albums, get_album_tracks, get_track_lyrics
from sqlalchemy import exc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Deja1218@localhost/hiphop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Alchemist"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"

###### set up 
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

######## index, signup, login, logout
@app.route('/')
def show_index():
    """ if no user redirect to signup page or go to index """

    if not g.user:
        return redirect('/signup')

    
    return render_template('/user-home.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def home():
    """ render signup form and index after signup """
    
    form = Signup()

    try:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            img_url = form.img_url.data or form.img_url.default
            new_user = User.signup(username=username, password=password, img_url=img_url)

            db.session.commit()
            do_login(new_user)
            return redirect('/')
    except:
        flash('Error signing up. Please try again', 'danger')
        return redirect('/')

    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ login user and return user page """

    form = Login()
    if form.validate_on_submit():
        user = User.login(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f'Welcome, {user.username}', 'success')
            return redirect(f'/user/{user.id}')
        else:
            flash('Login Unsuccessful', 'danger')
            redirect('/login')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ logout user and redirect to login page """

    do_logout()
    return redirect("/login")

###### user and post routes ########

@app.route('/all-users')
def show_all_users():
    """ shows all users """

    curr_user = g.user
    users = [user for user in User.query.all() if user.id != curr_user.id]
    return render_template('all-users.html', users=users)

@app.route('/user/<int:id>')
def view_user(id):
    """ displays the home page for the current user with post of followed users """

    user = User.query.get(id)
    if user:
        following_ids = [f.id for f in g.user.following] + [g.user.id]

        posts = (Post
                    .query
                    .filter(Post.user_id.in_(following_ids))
                    .order_by(Post.timestamp.desc())
                    .limit(100)
                    .all())
    return render_template('user-home.html', user=user, posts=posts)

@app.route('/post/<int:user_id>', methods=['GET', 'POST'])
def make_post(user_id):
    """ allows current user to make a post """

    form = PostForm()

    if form.validate_on_submit():
        text = form.text.data
        new_post = Post(user_id=user_id, text=text)
        
        db.session.add(new_post)

        db.session.commit()

        return redirect(f'/user/{g.user.id}')
    return render_template('post.html', form=form)

@app.route('/post/delete/<int:id>', methods=['POST'])
def delete_post(id):
    """ delete a post """

    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/user/{g.user.id}')

@app.route('/follow/<int:followed_id>')
def follow_users(followed_id):
    """ set the follows for logged in user """
   
    followed_user = User.query.get(followed_id)
    g.user.following.append(followed_user)

    db.session.commit()
    return redirect(f'/user/{g.user.id}')

@app.route('/followers')
def view_followers():
    """ view all current users followers """

    user = g.user
    return render_template('followers.html', user=user)

@app.route('/following')
def view_following():
    """ view all users current user is following """

    user = g.user
    return render_template('following.html', user=user)


@app.route('/like/<int:post_id>')
def like_post(post_id):
    """ allows logged in user to like a post """

    post = Post.query.get(post_id)

    if post not in g.user.likes:
        g.user.likes.append(post)
        db.session.commit()
        return redirect(f'/user/{g.user.id}')
        
    if post in g.user.likes:
        g.user.likes.remove(post)
        db.session.commit()
        return redirect(f'/user/{g.user.id}')

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    """ edit logged in user """

    form = Edit()
    user = User.query.get(id)

    if form.validate_on_submit():
        user.username = user.username if form.username.data == '' else form.username.data
        user.img_url = user.img_url if form.img_url.data == '' else form.img_url.data or form.img_url.default

        db.session.commit()
        return redirect(f'/user/{id}')
    
    return render_template('edit-user.html', form=form, user=user)


@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Delete logged in user."""

    do_logout()
    
    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

########## artist and music related routes 

@app.route('/add-artist', methods=['GET', 'POST'])
def add_artist():
    """ creates an artist and stored it """
    
    form = AddArtist()
    if form.validate_on_submit():
        try:
            name = form.name.data
            img = form.img_url.data or form.img_url.default
            new_artist = Artist(name=name, artist_id=get_artist_id(name), img_url=img)
            db.session.add(new_artist)
            db.session.commit()
            return redirect('/add-artist')
        except:
            flash('Error Adding Artist', 'danger')
            db.session.rollback()
            return redirect('/add-artist')
    artist = Artist.query.all()
    return render_template('add-artist.html', form=form, artist=artist)

@app.route('/artist/<int:id>')
def artist_profile(id):
    """ get the artist albums """

    artist = Artist.query.get(id)
    albums = get_artist_albums(artist.artist_id)
    return render_template('artist-profile.html', artist=artist, albums=albums)

@app.route('/album-tracks/<int:id>')
def show_album_tracks(id):
    """ get artist albums track list """

    track = get_album_tracks(id)
    tracks = list(track.keys())
    ids = list(track.values())

    return render_template('tracks.html', track=track, ids=ids )

@app.route('/track/lyrics/<int:track_id>')
def read_lyrics(track_id):
    """ get lyrics for tracks """

    lyrics = get_track_lyrics(track_id)
    return render_template('lyrics.html', lyrics=lyrics)
