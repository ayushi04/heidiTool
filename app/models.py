import json
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name="", phone="", password="", email=""):
        self.email = email
        self.phone = phone
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User %s %s>" % (self.id, self.name)


#t1 in neo4j
# class Image(db.Model, UserMixin):
#     __tablename__ = 'image'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100),nullable=False)
#     tlx = db.Column(db.Integer,nullable=False)
#     tly = db.Column(db.Integer,nullable=False)
#     brx = db.Column(db.Integer,nullable=False)
#     bry = db.Column(db.Integer,nullable=False)
#     color = db.Column(db.String(400),nullable=False)
#     label = db.Column(db.Integer,nullable=False)
#     block_col = db.Column(db.Integer,nullable=False)
#     block_row = db.Column(db.Integer,nullable=False)
#     #email = db.Column(db.String(100), unique=True, nullable=False)
#     #name = db.Column(db.String(100), nullable=False)
#     #phone = db.Column(db.Integer, nullable=False, unique=True)
#     #password = db.Column(db.String(80), nullable=False)

#     def __init__(self, name="", tlx="", tly="", brx="",bry="",color="",block_row="",block_col=""):
#         self.tlx = tlx
#         self.tly = tly
#         self.name = name
#         self.brx = brx
#         self.bry = bry

#     def __repr__(self):
#         return "<image %s %s>" % (self.id, self.name)

'''
class Image(db.Model, UserMixin):
    __table__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    tlx = db.Column(db.Integer,nullable=False)
    tly = db.Column(db.Integer,nullable=False)
    brx = db.Column(db.Integer,nullable=False)
    bry = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(400),nullable=False)
    block_col = db.Column(db.Integer,nullable=False)
    block_row = db.Column(db.Integer,nullable=False)

    def __init__(self, name="", tlx="", tly="", brx="",bry="",color="",block_row="",block_col=""):
        self.tlx = tlx
        self.tly = tly
        self.name = name
        self.brx = brx
'''    

class HeidiMatrix(db.Model, UserMixin):
    __tablename__ = 'heidi_matrix'
    id = db.Column(db.Integer, primary_key=True)
    subspace = db.Column(db.Integer,nullable=False)
    row_index = db.Column(db.Integer,nullable=False)
    col_index = db.Column(db.Integer,nullable=False)
    dataset = db.Column(db.String(100),nullable=False)
    value = db.Column(db.Integer,nullable=False)

    def __init__(self, subspace="", row_index="", col_index="", dataset="", value=""):
        self.subspace = subspace
        self.row_index = row_index
        self.col_index = col_index
        self.value = value
        self.dataset = dataset

    def __repr__(self):
        return "<heidi_matrix %s %s>" % (self.id, self.subspace)

class Legend(db.Model, UserMixin):
    __tablename__ = 'legend'
    dataset = db.Column(db.String(100), primary_key=True,nullable=False)
    subspace = db.Column(db.Integer, primary_key=True,nullable=False)
    dimensions = db.Column(db.String,nullable=False)  # Use a text column to store the serialized list
    
    def __init__(self, dataset = "", subspace = "", dimensions = []):
        self.dataset = dataset
        self.subspace = subspace
        self.dimensions = json.dumps(dimensions)
        
    # def set_dimensions(self, dimensions):
    #     self.dimensions = json.dumps(dimensions)

    # def get_dimensions(self):
    #     return json.loads(self.dimensions)
    
class Dataset(db.Model, UserMixin):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    dataset = db.Column(db.String(100),nullable=False)
    no_of_rows = db.Column(db.Integer,nullable=False)
    no_of_cols = db.Column(db.Integer,nullable=False)
    column_names_list = db.Column(db.String)  # Use a text column to store the serialized list

    def __init__(self, dataset="", no_of_rows="", no_of_cols="", column_names_list=[]):
        self.dataset = dataset
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.column_names_list = json.dumps(column_names_list)
        
    def set_column_names_list(self, column_names_list):
        self.column_names_list = json.dumps(column_names_list)
    
    def get_column_names_list(self):
        return json.loads(self.column_names_list)
    
    def __repr__(self):
        return "<dataset %s %s>" % (self.id, self.dataset)
    

    