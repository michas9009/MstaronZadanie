from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.body} - {self.userId}"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.surname}"


db.create_all()

#-------------------------------------------
#HOME PAGE
#-------------------------------------------
@app.route("/")
def home():
    posts_list = db.session.query(Posts).all()
    return render_template("index.html", todo_list=posts_list)

#-------------------------------------------
#POSTS (articles)
#s terminalom/postman/...
#-------------------------------------------
@app.route("/posts")
def posts():
    posts = Posts.query.all()
    output = []

    # vyhladavanie s argumentom
    id = request.args.get("id")
    userId = request.args.get("userId")

    #vyhladavanie podla ID
    if id:
        for post in posts:
            if post.id == int(id):
                post_data = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}
                output.append(post_data)
        return {"posts": output}

    #vyhladavanie podla userId
    elif userId:
        for post in posts:
            if post.userId == int(userId):
                post_data = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}
                output.append(post_data)
        return {"posts": output}

    #vyhladavanie bez argumentu
    for post in posts:
        post_data = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}
        output.append(post_data)

    return {"posts": output}

#konkretny clanok
@app.route("/posts/<id>")
def get_post(id):
    post = Posts.query.get_or_404(id)
    return {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}

#pridat clanok
@app.route("/posts", methods=["POST"])
def add_post():
    post = Posts(userId=request.json["userId"], title=request.json["title"], body=request.json["body"])
    db.session.add(post)
    db.session.commit()
    return {"id": post.id}

#vymazat clanok
@app.route("/posts/<id>", methods=["DELETE"])
def delete_post(id):
   post = Posts.query.get(id)
   if post is None:
       return {"error": "post not found..."}
   db.session.delete(post)
   db.session.commit()
   return {"message": "DELETED"}

#-----------------------------------------
# FOR FRONTEND
#-----------------------------------------

#search
@app.route("/search_post", methods=["GET", "POST"])
def search_post():

    search_by = request.form.get("search_by")
    searching_for = request.form.get("searching_for")

    if search_by == "by_id":
        search_result = db.session.query(Posts).filter_by(id=searching_for).all()
    else:
        search_result = db.session.query(Posts).filter_by(userId=searching_for).all()

    return render_template("index.html", todo_list=search_result)

#ADD POST (article)
@app.route("/add_post_w_form", methods=["POST"])
def add_post_w_form():
    title = request.form.get("title")
    body = request.form.get("body")
    userId = request.form.get("userId")

    #test ci user existuje
    userTest = Users.query.all()
    for user in userTest:
        if int(userId) == user.id:
            # new_post = Posts(userId=request.json["userId"], title=request.json["title"], body=request.json["body"])
            new_post = Posts(userId=userId, title=title, body=body)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("home"))
            # return (message, redirect(url_for("home")))

    return redirect(url_for("home"))

#UPDATE POST (article)
@app.route("/update_post_w_form", methods=["PUT", "GET", "POST"])
def update_post_w_form():
    id = request.form.get("id")
    userId = request.form.get("userId")
    title = request.form.get("title")
    body = request.form.get("body")

    postInDB = Posts.query.get(id)

    if int(id) == postInDB.id:
        postInDB.title = title
        postInDB.body = body

    db.session.commit()
    return redirect(url_for("home"))

#vymazanie clanku
@app.route("/del_post_w_form/<int:id>", methods=["DELETE", "GET"])
def del_post_w_form(id):
    post = Posts.query.get(int(id))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))


#----------
# USERS
#pouzivatelia...
#-----------
@app.route("/users")
def users():
    users = Users.query.all()
    posts = Posts.query.all()
    output = []

    # vyhladavanie s argumentom
    id = request.args.get("id")
    # vyhladavanie podla ID (vsetky jeho lcanky)
    if id:
        for post in posts:
            if post.userId == int(id):
                post_data = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}
                output.append(post_data)
        return {"posts": output}

    for user in users:
        user_data = {"id": user.id, "name": user.name, "surname": user.surname}
        output.append(user_data)

    return {"users": output}

@app.route("/users/<id>")
def get_user(id):
    user = Users.query.get_or_404(id)
    return {"id": user.id, "name": user.name, "surname": users.surname}

@app.route("/users", methods=["POST"])
def add_user():
    user = Users(name=request.json["name"], surname=request.json["surname"])
    db.session.add(user)
    db.session.commit()
    return {"id": user.id}


if __name__ == "__main__":
    app.run()

