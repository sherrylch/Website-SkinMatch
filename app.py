import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import error

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies).
# False so that once webpage closes info goes away and they have to relogin
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# use SQLite to access database skinmatch.db located in project folder
connection = sqlite3.connect("skinmatch.db", check_same_thread=False)
connection.row_factory = sqlite3.Row
db = connection.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products", methods=["GET","POST"])
def products():
    # Products ordered by brand so that if in future more are added in different order they are still displayed by brand on app.
    if request.method == "POST":
        brand = request.form.get("search")
        search = brand.strip().upper()

        product = db.execute("SELECT * FROM products WHERE search LIKE ? ORDER BY brand", ("%" + search + "%",))
        product = [dict(row) for row in product.fetchall()]
        return render_template("products.html", product=product)

    else:
        product = db.execute("SELECT * FROM products ORDER BY brand")
        product = [dict(row) for row in product.fetchall()]
        return render_template("products.html", product=product)


# Login check database for password/username
@app.route("/login", methods=["GET","POST"])
def login():
    # start by forgetting any session
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # check if username exist and if password is the same
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = [dict(row) for row in rows.fetchall()]

        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
            return error("Invalid username or Wrong Password")

        # if username is valid and password matches, we will remember id in session and redirect to mainpage
        else:
            session["user_id"]= rows[0]["id"]
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id currently logged in
    session.clear()

    # POST method add new user into the users database after checking for errors
    if request.method == "POST":
        # check that username was inputted
        if not request.form.get("username"):
            return error("Please input username")

        # check that password was inputted
        elif not request.form.get("password"):
            return error("Please input password")

        # check password and confirmation password matches
        elif request.form.get("password") != request.form.get("confirm_password"):
            return error("Password and Confirmation password Do NOT Match. Please Try Again")

        # check that email is valid by chacking that it has @ and .
        elif "@" not in request.form.get("email") and "." not in request.form.get("email"):
            return error("Invalid Email")

        # check that username is unique
        rows = db.execute("SELECT * FROM users WHERE username= ?", (request.form.get("username"),))
        rows = [dict(row) for row in rows.fetchall()]

        if len(rows) >= 1:
            return error("An account under this username already exist. Please select another username")

        # check if this email has been registered already
        email = db.execute("SELECT * FROM users WHERE email= ?", (request.form.get("email"),))
        email = [dict(row) for row in email.fetchall()]

        if len(email) >= 1:
            return error("There is an account under this email already")

        # if no errors add user into database
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            hash = generate_password_hash(password)
            email = request.form.get("email")

            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", (username, hash, email))
            connection.commit()

            # once registered and data inserted into database, log in user using the id
            user = db.execute("SELECT id FROM users WHERE username = ?", (username,))
            user = [dict(row) for row in user.fetchall()]
            session["user_id"] = user[0]["id"]
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/infallibleconcealer", methods=["GET","POST"])
def infallible_concealer():
    if request.method == "POST":
        if session.get("user_id") is None:
            return error("Please Register/Login First")

        elif not request.form.get("upload-img"):
            return error("No image Selected")

        elif not request.form.get("confirm_img"):
            return error("Please check the checkbox to confirm image upload")

        user_id = session["user_id"]
        img_des = request.form.get("img-des")
        img_url = request.form.get("imgUrl")

        # insert new image info into database using url
        db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Infallible Full Wear Waterproof Concealer')", (user_id, img_des, img_url))
        connection.commit()

        # Get products from database and input in app
        shades = db.execute("SELECT * FROM shades WHERE product='Infallible Full Wear Waterproof Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]

        return render_template("infallibleconcealer.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Infallible Full Wear Waterproof Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("infallibleconcealer.html", shades=shades)




@app.route("/fitmeconcealer", methods=["GET", "POST"])
def fitmeconcealer():
    if request.method == "POST":
        if session.get("user_id") is None:
            return error("Please Register/Login First")

        elif not request.form.get("upload-img"):
            return error("No image Selected")

        elif not request.form.get("confirm_img"):
            return error("Please check the checkbox to confirm image upload")

        user_id = session["user_id"]
        img_des = request.form.get("img-des")
        img_url = request.form.get("imgUrl")

        # insert new image info into database using url
        db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Maybelline Fit Me Liquid Concealer')", (user_id, img_des, img_url))
        connection.commit()

        # Get products from database and input in app
        shades = db.execute("SELECT * FROM shades WHERE product='Maybelline Fit Me Liquid Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("fitmeconcealer.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Maybelline Fit Me Liquid Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("fitmeconcealer.html", shades=shades)


@app.route("/superstay", methods=["GET", "POST"])
def superstay():
        if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Super Stay Full Coverage Foundation')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='Super Stay Full Coverage Foundation' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]
            return render_template("superstay.html", shades=shades)

        else:
            shades = db.execute("SELECT * FROM shades WHERE product='Super Stay Full Coverage Foundation' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]
            return render_template("superstay.html", shades=shades)


@app.route("/milanifoundation", methods=["GET","POST"])
def milanifoundation():
    if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Conceal + Perfect 2-in-1 Foundation + Concealer')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='Conceal + Perfect 2-in-1 Foundation + Concealer' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]

            return render_template("milanifoundation.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Conceal + Perfect 2-in-1 Foundation + Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("milanifoundation.html", shades=shades)


@app.route("/elfconcealer", methods=["GET","POST"])
def elfconcealer():
    if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'elf Camo Hydrating Concealer')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='elf Camo Hydrating Concealer' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]
            return render_template("elfcamo.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='elf Camo Hydrating Concealer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("elfcamo.html", shades=shades)


@app.route("/wetnwild", methods=["GET","POST"])
def wetnwild():
    if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Photo Focus Dewy Foundation')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='Photo Focus Dewy Foundation' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]
            return render_template("wetnwild.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Photo Focus Dewy Foundation' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("wetnwild.html", shades=shades)


@app.route("/butterbronzer", methods=["GET","POST"])
def butterbronze():
    if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Butter Bronzer Murumuru Butter Bronzer')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='Butter Bronzer Murumuru Butter Bronzer' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]
            return render_template("butterbronze.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Butter Bronzer Murumuru Butter Bronzer' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("butterbronze.html", shades=shades)


@app.route("/elffoundation", methods=["GET","POST"])
def elffoundation():
    if request.method == "POST":
            if session.get("user_id") is None:
                return error("Please Register/Login First")

            elif not request.form.get("upload-img"):
                return error("No image Selected")

            elif not request.form.get("confirm_img"):
                return error("Please check the checkbox to confirm image upload")

            user_id = session["user_id"]
            img_des = request.form.get("img-des")
            img_url = request.form.get("imgUrl")

            # insert new image info into database using url
            db.execute("INSERT INTO shades (user_id, description, images, product) VALUES (?, ?, ?, 'Flawless Finish Foundation')", (user_id, img_des, img_url))
            connection.commit()

            # Get products from database and input in app
            shades = db.execute("SELECT * FROM shades WHERE product='Flawless Finish Foundation' ORDER BY id DESC")
            shades = [dict(row) for row in shades.fetchall()]

            return render_template("elffoundation.html", shades=shades)

    else:
        shades = db.execute("SELECT * FROM shades WHERE product='Flawless Finish Foundation' ORDER BY id DESC")
        shades = [dict(row) for row in shades.fetchall()]
        return render_template("elffoundation.html", shades=shades)




@app.route("/saved", methods=["GET","POST"])
def saved():
    if request.method == "POST":
        if session.get("user_id") is None:
            return error("Please Register/Login First")

        img_id = request.form.get("saved_img_id")
        user_id = session["user_id"]
        images = request.form.get("saved_images")
        product = request.form.get("saved_product")
        description = request.form.get("saved_description")
        date = datetime.now()

        db.execute("INSERT INTO saved (img_id, user_id, images, product, description, date) VALUES (?, ?, ?, ?, ?, ?)", (img_id, user_id, images, product, description, date))
        connection.commit()

        saved = db.execute("SELECT * FROM saved WHERE user_id=? GROUP BY img_id ORDER BY date DESC", (user_id,))
        saved = [dict(row) for row in saved.fetchall()]
        return render_template("saved.html", saved=saved)
    else:
        # return saved list based of user_id, order by date DESC so newest added show up first
        user_id = session["user_id"]

        saved = db.execute("SELECT * FROM saved WHERE user_id=? GROUP BY img_id ORDER BY date DESC", (user_id,))
        saved = [dict(row) for row in saved.fetchall()]
        return render_template("saved.html", saved=saved)


@app.route("/delete_saved", methods=['POST'])
def delete_saved():
    user_id = session["user_id"]
    delete_id = request.form.get("delete_id")

    db.execute("DELETE FROM saved WHERE user_id = ? AND img_id = ?", (user_id, delete_id))
    connection.commit()

    saved = db.execute("SELECT * FROM saved WHERE user_id=? GROUP BY img_id ORDER BY date DESC", (user_id,))
    saved = [dict(row) for row in saved.fetchall()]
    return render_template("saved.html", saved=saved)


if __name__ == '__main__':
    app.run(debug=True)


