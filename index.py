from flask import Flask, render_template, url_for, redirect, request, session
import datetime
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from wtforms import StringField, SubmitField, PasswordField, HiddenField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

def validate_cedula(self, cedula):
        existing_user_cedula = User.query.filter_by(
            cedula=cedula.data).first()
        if existing_user_cedula:
            raise ValidationError(
                'La cedula ya existe. Por favor inicie sesión.')

# CLASES DE LOS FORMULARIOS ---INICIO---
class LoginForm(FlaskForm):
    cedula = StringField('Cedula', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    fullname = StringField('Nombre Completo', validators=[DataRequired(), Length(min=4, max=20)])
    cedula = StringField('Cedula', validators=[DataRequired(), Length(min=8, max=20), validate_cedula])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Telefono', validators=[DataRequired()])
    factura = IntegerField('Nro. Factura', validators=[DataRequired()])
    submit = SubmitField('Crear Cuenta')

class NewTicketForm(FlaskForm):
    title = StringField('Asunto', validators=[DataRequired(), Length(min=4, max=200)])
    product = SelectField('Seleccionar Producto', validators=[DataRequired()])
    description = TextAreaField('Descripcion', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Crear Ticket')

# CLASES DE LOS FORMULARIOS ---FINAL---

class Base(DeclarativeBase):
  pass

# INICIALIZAMOS FLASK, CONFIGURAMOS ACCESO A LA BASE DE DATOS Y EL USO DEL ORM (SQLAlchemy)
app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://usuario:password@localhost:3306/mydb"
db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt(app)

# INICIALIZAMOS EL GESTOR DE SESIONES
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# CONFIGURAMOS LA CARGA DE SESION DE USUARIO (empleado o cliente)
@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(cedula=user_id).first()
    if user:
        return user
    else:
        return Empleado.query.filter_by(cedula=user_id).first()

# INICIAMOS EL ORM Y CARGAMOS LAS DEFINICIONES DE TABLAS
db.init_app(app)
with app.app_context():
    db.reflect()

# TABLAS DE LA BASE DE DATOS/MODELOS ---INICIO---
class User(db.Model, UserMixin):
    __table__ = db.metadata.tables["cliente"]

    def get_id(self):
        return (self.cedula)

class Ticket(db.Model):
    __table__ = db.metadata.tables["ticket"]

class HistorialTicket(db.Model):
    __table__ = db.metadata.tables["historial_ticket"]

class ResponsableTicket(db.Model):
    __table__ = db.metadata.tables["responsable_ticket"]

class DetalleFactura(db.Model):
    __table__ = db.metadata.tables["detalle_factura"]

class Empleado(db.Model, UserMixin):
    __table__ = db.metadata.tables["empleado"]

    def get_id(self):
        return (self.cedula)

class Producto(db.Model):
    __table__ = db.metadata.tables["producto"]

class Garantia(db.Model):
    __table__ = db.metadata.tables["garantia"]

class Factura(db.Model):
    __table__ = db.metadata.tables["factura"]

# TABLAS DE LA BASE DE DATOS/MODELOS ---FINAL---


# RUTAS DE LA APLICACION Y LOGICA DEL NEGOCIO ---INICIO---
@app.route("/")
def main():
    return render_template('main.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('dashboard'))

    # usamos el formulario de login
    form = LoginForm()

    #validamos cuando lo envien
    if form.validate_on_submit():

        #hacemos un query a la base de datos (SELECT WHERE...)
        user = User.query.filter_by(cedula=form.cedula.data).first()

        #validamos si el usuario es un cliente o un empleado
        if user != None:

            #comparamos el hash de la contrasena
            if bcrypt.check_password_hash(user.contrasena, form.password.data):

                #logueamos al usuario y redirijimos al dashboard
                login_user(user)
                return redirect(url_for('dashboard'))
        else:
            user = Empleado.query.filter_by(cedula=form.cedula.data).first()
            if user:
                if bcrypt.check_password_hash(user.contrasena, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('dashboard'))

    form = RegisterForm()
    message = ''
    if form.validate_on_submit():

        factura = Factura.query.filter_by(id=form.factura.data).first()

        if(factura):
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                cedula=form.cedula.data, 
                contrasena=hashed_password, 
                nombre=form.fullname.data, 
                correo=form.email.data,
                telefono=form.telefono.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            message = 'No hay ningun cliente con esta factura.'


    return render_template('register.html',form=form, message=message)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    tickets = []
    if current_user.__class__ == User:
        tickets = Ticket.query.filter_by(id_cliente=current_user.id_cliente)
    else:
        resp_tickets = ResponsableTicket.query.filter_by(id_empleado=current_user.id_empleado)
        
        for resp in resp_tickets:
            tickets = Ticket.query.filter_by(id=resp.id_ticket)

        for ticket in tickets:
            ticket.cliente = User.query.filter_by(id_cliente=ticket.id_cliente).nombre

    return render_template('dashboard.html', tickets=tickets)




@app.route("/new-ticket", methods=['GET', 'POST'])
@login_required
def newTicket():

    form = NewTicketForm()
    
    facturas = Factura.query.filter_by(id_cliente=current_user.id_cliente).all()

    for factura in facturas:
        detalle_facturas = DetalleFactura.query.filter_by(id_factura=factura.id).all()

    tuplas = []
    for detalle in detalle_facturas:
        product = Producto.query.filter_by(id=detalle.id_producto).first()
        tuplas.append((getattr(product, 'id'), getattr(product, 'nombre')))

    form.product.choices = tuplas

    if form.validate_on_submit():
        new_ticket = Ticket(
            id_producto=form.product.data,
            id_cliente=current_user.id_cliente, 
            asunto=form.title.data,
            descripcion=form.description.data,
            status='ABIERTO',
            fecha_creacion=datetime.datetime.now(), 
            fecha_cierre=datetime.datetime.now() + datetime.timedelta(days=5)
        )
        print(new_ticket)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    return render_template('new_ticket.html', form=form)

# RUTAS DE LA APLICACION Y LOGICA DEL NEGOCIO ---FINAL---