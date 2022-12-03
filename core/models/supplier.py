from extensions import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

