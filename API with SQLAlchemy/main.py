from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/post'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    author = db.Column(db.String(50))
    
    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.author = author

class PostSchema(ma.Schema):
    class Meta:
        fields = ("title", "author", "description")
 
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/post', methods=['POST'])
def add_post():
    title=request.json['title']
    desc=request.json['description']
    author=request.json['author']

    my_posts=Post(title,desc,author)
    db.session.add(my_posts)
    db.session.commit()
    
    return post_schema.jsonify(my_posts)

@app.route("/get", methods=["GET"])
def get_post():
    all_posts=Post.query.all()
    result=posts_schema.dump(all_posts) #The dump() method is used when the Python objects have to be stored in a file.
    return jsonify(result)
 

@app.route('/get_details/<id>/', methods=['GET'])
def post_details(id):
    post=Post.query.get(id)
    return post_schema.jsonify(post)

@app.route('/update_post/<id>/', methods=['PUT'])
def update_post(id):
    post=Post.query.get(id)

    title=request.json['title']
    descrption=request.json['description']
    author=request.json['author']

    post.title=title
    post.description=descrption
    post.author=author

    db.session.commit()
    return post_schema.jsonify(post)

@app.route('/delete_post/<id>/', methods=['DELETE'])
def delete_post(id):
    post=Post.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)



if __name__== "__main__":
    app.run(debug=True)