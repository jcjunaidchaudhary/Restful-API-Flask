from os import name
from flask import Flask ,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import csv
import io
import openpyxl
from flask_marshmallow import Marshmallow

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/apitest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    rollno=db.Column(db.Integer, unique=True) 
    std =db.Column(db.String(10))
    course = db.Column(db.String(20))
    
    def __init__(self ,name, rollno, std, course):
        self.name=name
        self.rollno=rollno
        self.std = std
        self.course = course

class PostSchema(ma.Schema):
    class Meta:
        fields = ("name","rollno", "std", "course")
 
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#////practice purpose on
#marshmallow practice....

# all_posts=Students.query.all()
# result=posts_schema.dump(all_posts)
# print(result)

# col = Students.query.filter_by(rollno=31).first()
# result=post_schema.dump(col)
# print(result['name'])

# dbRollno= Students.query.with_entities(Students.rollno).all()
# result1=posts_schema.dump(dbRollno)
# print(result1)
#practice purpose off\\\\\


dbRollno= Students.query.with_entities(Students.rollno).all()
existing=[]
for x in dbRollno:
    lst=list(x)
    existing+=lst

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
                i+=1
                # name, std, course=row
                if i==1:
                    continue
                else:
                    if int(row[1]) in existing:
                        name = row[0]
                        std = row[2]
                        course = row[3]
                        col = Students.query.filter_by(rollno=row[1]).first()
                        if col.name!=name or col.std!=std or col.course!=course:
                            col.name=name
                            col.std=std
                            col.course=course
                            db.session.add(col) 
                        else:
                            continue
                    else:
                        my_posts=Students(*row)
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
                    if row[1] in existing:
                        name = row[0]
                        std = row[2]
                        course = row[3]
                        col = Students.query.filter_by(rollno=row[1]).first()
                        if col.name!=name or col.std!=std or col.course!=course:    
                            col.name=name
                            col.std=std
                            col.course=course
                            db.session.add(col)
                    else:
                        my_posts=Students(*row)
                        db.session.add(my_posts)
                    db.session.commit()
            return jsonify({'message' : 'Excel File successfully uploaded'})

@app.route("/get", methods=["GET"])
def get_post():
    details=Students.query.all()
    result=posts_schema.dump(details) 
    return jsonify(result)
 

if __name__== "__main__":
    app.run(debug=True)