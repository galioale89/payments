from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, DecimalField, SubmitField, SelectField, validators

class PaymentForm(FlaskForm):
    type = SelectField("Tipo", [validators.DataRequired()], choices=[(1, "A Pagar"),(2, "Pago")])
    description = TextAreaField("Descrição", [validators.DataRequired(), validators.Length(min=1, max=200)])
    code = StringField("Código", [validators.DataRequired(), validators.Length(min=1, max=20)])
    due_date = DateField("Data de Vencimento", [validators.DataRequired()])
    pay_date = DateField("Data de Pagamento", [validators.DataRequired()])
    value = DecimalField("Valor(R$)", [validators.DataRequired()])
    supplier = StringField("Fornecedor", [validators.DataRequired()])
    save = SubmitField("Salvar")
