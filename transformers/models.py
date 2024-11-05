from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Transformer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    affiliation = db.Column(db.String(300), nullable=False)
    abilities = db.Column(db.String(300))
    transformation_mode = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(1200))
    description = db.Column(db.Text(), nullable=False)
    quote = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"Transformer: {self.name} -- {self.affiliation}"
