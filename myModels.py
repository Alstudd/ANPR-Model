from db import db

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    originalImgData = db.Column(db.LargeBinary, nullable=False)
    originalImgURL = db.Column(db.Text, nullable=False)