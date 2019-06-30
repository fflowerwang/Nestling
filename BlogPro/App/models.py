from App.exts import db


class Lanmu(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),unique=True)
    another_name = db.Column(db.String(100),unique=True)
    articles = db.relationship('Article',backref='my_lanmu',lazy='dynamic')



class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),unique=True)
    cont = db.Column(db.String(4000))
    date = db.Column(db.DateTime,default='2018-10-12 11:12:40')
    tag = db.Column(db.String(50),default='PHP、JavaScript')
    press = db.Column(db.Integer,default=0)
    lanmu = db.Column(db.Integer,db.ForeignKey(Lanmu.id))


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),unique=True)
    passwd = db.Column(db.String(50))







