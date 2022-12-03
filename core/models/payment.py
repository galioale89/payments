from extensions import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    pay_date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.DECIMAL(8,2), nullable=False)
    id_supplier = db.Column(db.Integer, foreign_key=True, nullable=True)

    def __repr__(self):
        return "<Payment(description='%s', type='%s', value='%s')>" % (
            self.description,
            self.type,
            self.value
        )

