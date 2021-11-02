from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import csv
from werkzeug.utils import secure_filename
import io
import openpyxl


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/apitest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20)) 
    std =db.Column(db.Integer)
    course = db.Column(db.String(40))
    
    def __init__(self ,name, std, course):
        self.name=name
        self.std = std
        self.course = course

class PostSchema(ma.Schema):
    class Meta:
        fields = ("name", "std", "course")
 
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


# @app.route('/post', methods=['POST'])
# def add_post():
#     title=request.json['name']
#     desc=request.json['descriptios']
#     author=request.json['author']

#     my_posts=Post(title,desc,author)
#     db.session.add(my_posts)
#     db.session.commit()
    
#     return post_schema.jsonify(my_posts)

# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         binaryData = csv.reader()
#         i=0
#         for row in binaryData:
#             i+=1
#             name, std, course=row
#             if i==1:
#                 continue
#             else:
#                 my_posts=Student(name, std, course)
#                 db.session.add(my_posts)
#                 db.session.commit()
#     return binaryData

@app.route('/csvUpload', methods=['POST'])
def csvUpload():
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            data = uploaded_file.stream.read() # This line uses the same variable and worked fine
            #Convert the FileStorage to list of lists here.

            stream = io.StringIO(data.decode("UTF8"), newline=None)
            reader = csv.reader(stream)
            i=0
            for row in reader:
                print(row) 
                i+=1
                # name, std, course=row
                if i==1:
                    continue
                else:
                    my_posts=Student(*row)
                    db.session.add(my_posts)
                    db.session.commit()

            return jsonify({'message' : 'csv file successfully uploaded'})

@app.route('/excelUpload',methods=['POST'])
def excelUpload():
    if request.method=='POST':
        if request.files:
            uploaded_file = request.files['filename']
            wb_obj=openpyxl.load_workbook(uploaded_file)
            sheet=wb_obj.active
            l=0
            for row in sheet.values:
                l+=1
                if l==1:
                    continue
                else:
                    my_posts=Student(*row)
                    db.session.add(my_posts)
                    db.session.commit()
            return jsonify({'message' : 'Excel File successfully uploaded'})






@app.route("/data", methods=['GET','POST'])
def data():
    if request.method=='POST':
        print('hello')
        file = request.files['data']
        data = file.stream.read()
        stream = io.StringIO(data.decode("UTF8"), newline=None)
        readit=csv.reader(stream)
        print("data", data.stream.read())
        print("data Type", type(data))
        for i in readit:
            print('i',i)
        

        # with open(file) as f:
        #     readit=csv.reader(f)
        #     i=0
        #     for row in readit:
        #         i+=1
        #         name, std, course=row
        #         if i==1:
        #             continue
        #         else:
        #             my_posts=Student(name, std, course)
        #             db.session.add(my_posts)
        #             db.session.commit()
        # return jsonify(
        #     # summary=make_data(data),
        #     csv_name=secure_filename(data.filename)
        # )
       
    return jsonify({'message' : 'File successfully uploaded'})




if __name__== "__main__":
    app.run(debug=True)

