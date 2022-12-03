from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.forms.payment import PaymentForm
from core.models.payment import Payment
from core.models.supplier import Supplier
import locale
from extensions import db

payment = Blueprint("payment", __name__, template_folder="templates")
api = '/payment'

@payment.route(f'{api}/')
def index():
    payment_list = Payment.query.order_by(Payment.id).all()

    for item in payment_list:
        if (item.description == 'RESRE'):
            item.description = 'Teste'

        date = item.pay_date
        date = (f'{date.strftime("%d")}/{date.strftime("%m")}/{date.strftime("%Y")}')
        item.pay_new_date = date

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        locale_value = locale.currency(item.value, grouping=True, symbol=None)
        item.new_value = locale_value

        if (item.id_supplier != None):
            filter_supplier = Supplier.query.filter_by(id=item.id_supplier).first()
            supplier_name = filter_supplier.name
            item.supplier_name = supplier_name

        if item.type == 2:
            item.type_paid = True
        else:
            item.type_paid = False

    return render_template('list.html', titulo='Pagamentos', payments=payment_list)


@payment.route(f'{api}/new')
def new():

    if "loguser"not in session or session["loguser"] == None:
        return redirect(url_for("logon.login", next=url_for("payment.new")))

    form = PaymentForm()
    supplier_list = Supplier.query.order_by(Supplier.id)
    return render_template('register.html', titulo='Lançar Pagamento', form=form, suppliers=supplier_list)


@payment.route(f'{api}/create', methods=['POST', ])
def create():

    form = PaymentForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    code = form.code.data
    type = form.type.data
    description = form.description.data
    due_date = form.due_date.data
    pay_date = form.pay_date.data
    value = form.value.data
    supplier = form.supplier.data

    new_payment = Payment(code=code, type=type, description=description, due_date=due_date, pay_date=pay_date,
                          value=value, id_supplier=supplier)
    db.session.add(new_payment)
    db.session.commit()

    flash('Pagamento adicionado!')
    return redirect(url_for('payment.index'))


@payment.route(f'{api}/new_pay/<int:id>')
def new_pay(id):

    if "loguser"not in session or session["loguser"] == None:
        return redirect(url_for("logon.login", next=url_for("payment.new")))

    payment = Payment.query.filter_by(id=id).first()
    form = PaymentForm()

    form.description.data = payment.description
    form.description.render_kw = {'readonly': True}
    form.code.data = payment.code
    form.code.render_kw = {'readonly': True}
    form.type.data = payment.type
    form.type.render_kw = {'readonly': True}
    form.due_date.data = payment.due_date
    form.due_date.render_kw = {'readonly': True}
    form.pay_date.data = payment.pay_date
    form.pay_date.render_kw = {'readonly': True}
    form.supplier.data = payment.id_supplier
    supplier_id = payment.id_supplier
    form.supplier.data = Supplier.query.filter_by(id=supplier_id).first().name
    form.supplier.render_kw = {'readonly': True}
    form.value.data = payment.value
    form.value.render_kw = {'readonly': True}
    form.save.render_kw = {'value': 'Pagar'}

    return render_template('payment.html', titulo='Pagar', id=id, form=form)


@payment.route(f'{api}/payment', methods=['POST', ])
def pay():
    form = PaymentForm(request.form)

    payment = Payment.query.filter_by(id=request.form['id']).first()
    payment.code = form.code.data

    payment.type = 2

    db.session.add(payment)
    db.session.commit()

    flash('Duplicata paga!')

    return redirect(url_for("payment.index"))


@payment.route(f'{api}/edit/<int:id>')
def edit(id):

    if "loguser"not in session or session["loguser"] == None:
        return redirect(url_for("logon.login", next=url_for("payment.new")))

    form = PaymentForm();

    supplier_list = Supplier.query.order_by(Supplier.id)
    payment = Payment.query.filter_by(id=id).first()

    form.code.data = payment.code
    form.description.data = payment.description
    form.due_date.data = payment.due_date
    form.pay_date.data = payment.pay_date
    form.value.data = payment.value

    supplier_id = payment.id_supplier
    supplier_name = Supplier.query.filter_by(id=supplier_id).first().name

    return render_template('edit.html', form=form, titulo=payment.code, id=id, suppliers=supplier_list,
                           supplier_id=supplier_id, supplier_name=supplier_name)


@payment.route(f'{api}/update', methods=['POST', ])
def update():

    if "loguser"not in session or session["loguser"] == None:
        return redirect(url_for("logon.login", next=url_for("payment.new")))

    form = PaymentForm(request.form)

    payment = Payment.query.filter_by(id=request.form['id']).first()

    payment.code = form.code.data
    payment.description = form.description.data
    payment.pay_date = form.pay_date.data
    payment.due_date = form.due_date.data
    payment.value = form.value.data
    payment.id_supplier = form.supplier.data

    db.session.add(payment)
    db.session.commit()

    flash('Duplicata atualizada!')

    return redirect(url_for("index"))



