from flask import Flask, render_template, request
from flask import redirect, make_response, jsonify
from flask import url_for, flash
from flask import session as login_session

from sqlalchemy import create_engine, asc, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Categories, Base, Items, Users

import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Home route


@app.route('/')
@app.route('/home')
def showHome():
    """
    Simply fetches all the categories in the database
    and the lateset 5 items in the items table
    and pass them to the home.html template
    """
    categories = session.query(Categories)
    sql = text("""
            SELECT items.name, categories.name,items.cat_id, items.id
            FROM items JOIN categories
            ON items.cat_id = categories.id
            order by items.id desc
            limit 5
            """)
    latestItems = session.execute(sql)
    return render_template("home.html",
                           categories=categories,
                           latestItems=latestItems
                           )

# Category route


@app.route("/category_items/<cat_id>")
def showCategoryItems(cat_id):
    """
    Takes in the category id and fetches its items, name
    from the database and pass them along with all the
    categories (to ues their names in the left side bar)
    to the categoryItems.html template to display them.
    """
    categories = session.query(Categories)
    items = session.query(Items).filter_by(cat_id=cat_id).all()
    category_name = session.query(Categories.name).filter_by(id=cat_id).all()
    return render_template("categoryItems.html",
                           items=items,
                           cat_name=category_name,
                           categories=categories
                           )

# The route to the JSON of the category route


@app.route("/category_items/<cat_id>/JSON")
def showCategoryItemsJSON(cat_id):
    """
    Takes in the category id and fetches all its
    items from the database and return the json format
    of this data.
    """
    category = session.query(Categories).filter_by(id=cat_id).one()
    items = session.query(Items).filter_by(cat_id=cat_id)
    return jsonify(Category=[category.serialize(items)])

# Single item route


@app.route("/category_items/<cat_id>/item/<item_id>")
def showItem(cat_id, item_id):
    """
    Takes in the category id and the item id
    and fetches the item data and pass it to the
    item.hmtl template to render them.
    """

    item = session.query(Items).filter_by(
        cat_id=cat_id).filter_by(id=item_id).one()
    return render_template("item.html", item=item)

# The route to the JSON of the single item route


@app.route("/category_items/<cat_id>/item/<item_id>/JSON")
def showItemJSON(cat_id, item_id):
    """
    Does the same as the single item route but returns
    the json format of the data.
    """

    item = session.query(Items).filter_by(
        cat_id=cat_id).filter_by(id=item_id).one()
    return jsonify(Item=[item.serialize])

# Add item route


@app.route("/add_item", methods=["GET", "POST"])
def addItem():
    """
    It first checks if the user is logged in if not
    it redirects to the home, if yes it renders the
    add form on GET request, and adds the data to
    the database on POST requests.
    """
    if "username" in login_session:
        if request.method == "POST":
            category = session.query(Categories).filter_by(
                id=request.form['category']).one()
            user = session.query(Users).filter_by(
                id=login_session['user_id']).one()
            item = Items(cat_id=request.form['category'],
                         name=request.form['title'],
                         user_id=login_session['user_id'],
                         description=request.form['description'],
                         cat=category,
                         user=user)

            session.add(item)
            session.commit()
            flash("Item added successfully")
            return redirect(url_for("showHome"))
        else:
            return render_template("add.html")
    else:
        return redirect(url_for("showHome"))

# Edit item route


@app.route("/editItem/<item_id>", methods=["GET", "POST"])
def editItem(item_id):
    """
    It first fetches the data of the item based on the
    passed item id, then checks if the user is logged
    in and owns the item, if not it redirects to the
    home page, if yes it passes the item data to the
    edit.html template to render them in the edit form
    on GET requests, and updates the data in the database
    on POST requests.
    """

    item = session.query(Items).filter_by(id=item_id).one()
    if "username" in login_session \
            and item.user_id == login_session['user_id']:
        if request.method == "POST":
            prev_name = item.name
            if request.form["title"]:
                item.name = request.form["title"]
            if request.form["description"]:
                item.description = request.form["description"]
            if request.form["category"]:
                item.cat_id = request.form["category"]
            session.add(item)
            session.commit()
            flash("The item %s was updated successfully" % prev_name)
            return redirect(url_for("showHome"))
        else:
            return render_template("edit.html", item=item)
    else:
        return redirect(url_for("showHome"))

# Delete item route


@app.route("/delete/<cat_id>/<item_id>", methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    """
    Fetches the data of the item based on the passed
    item id, and checks if the user is logged in and owns
    the item, if not it redirects to the home. If yes, it
    passes the data of the item to the delete.html template
    to on GET requests to make the user confirm the delete,
    and deletes the item on POST requests.
    """

    item = session.query(Items).filter_by(
        cat_id=cat_id).filter_by(id=item_id).one()
    category = session.query(Categories).filter_by(id=cat_id).one()
    if "username" in login_session \
            and item.user_id == login_session['user_id']:
        if request.method == "POST":
            session.delete(item)
            session.commit()
            flash("Item %s has been deleted successfully." % item.name)
            return redirect(url_for("showHome"))
        else:
            return render_template("delete.html",
                                   cat_name=category.name,
                                   item_name=item.name)
    else:
        return redirect(url_for('showHome'))

# The route for the JSON of the home route


@app.route("/catalog.json")
def catalagJSON():
    """
    Fetches all the categories and theire items and
    return the json format of the data.
    """
    categories = session.query(Categories).all()
    items = session.query(Items)
    return jsonify(Categories=[i.serialize(items) for i in categories])

# Login route


@app.route('/login')
def showLogin():
    """
    Checks if the user is logged in, if yes it redirects
    to the home page. If not , it randomly generates a state
    token and pass it to the login.html template to complete
    the login and render the button to login.
    """
    if "username" not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    return redirect(url_for("showHome"))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    g_id = credentials.id_token['sub']
    if result['user_id'] != g_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and g_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = g_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = 'Welcome, %s' % login_session['username']
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']

        flash("You have successfully been logged out.")
        return redirect(url_for('showHome'))
    else:
        flash("Failed to revoke token for given user.")
        return redirect(url_for('showHome'))


def createUser(login_session):
    newUser = Users(name=login_session['username'], email=login_session[
        'email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
