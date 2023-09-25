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
    
class Dataset(db.Model, UserMixin):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    dataset = db.Column(db.String(100),nullable=False)
    rows = db.Column(db.Integer,nullable=False)
    cols = db.Column(db.Integer,nullable=False)

    def __init__(self, dataset="", rows="", cols=""):
        self.dataset = dataset
        self.rows = rows
        self.cols = cols

    def __repr__(self):
        return "<dataset %s %s>" % (self.id, self.dataset)
    

    