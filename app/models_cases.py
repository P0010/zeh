from app import db
from datetime import datetime

# Контакты

class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    script = db.Column(db.Text)
    weekdays = db.Column(db.String)
    saturday = db.Column(db.String)
    sunday = db.Column(db.String)
    phones = db.relationship("Phone", cascade='all,delete', backref='contact', lazy='dynamic')

class ContactsTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(300))

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)
    id_contact = db.Column(db.Integer, db.ForeignKey('contacts.id'))


# Кейсы

subs_cases = db.Table('subs_cases',
                       db.Column('cases_id', db.ForeignKey('cases.id')),
                       db.Column('product_id', db.ForeignKey('products.id'))
)

class Cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String)
    intro = db.Column(db.Text)
    title2 = db.Column(db.String(200)) 
    description = db.Column(db.String(300))
    image = db.relationship("Images_cases", cascade='all,delete', backref='case', lazy='dynamic')
    uslugi = db.relationship("Product", secondary=subs_cases, backref=db.backref('case'))
    keys = db.relationship("Keys_cases", cascade='all,delete', backref='case')

class CasesTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(300))

class Images_cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    alt = db.Column(db.String) # new

class Keys_cases(db.Model):
    __tablename__ = 'keys_cases'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text(1500))
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    images = db.relationship("Images_key_cases", cascade="all,delete", backref='keys_cases')

class Images_key_cases(db.Model):
    __tablename__ = 'images_key_cases'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    alt = db.Column(db.String(100))
    keys_id = db.Column(db.Integer, db.ForeignKey('keys_cases.id'))


# О нас

class Aboutus(db.Model):
    __tablename__ = 'aboutus'
    id = db.Column(db.Integer, primary_key=True)
    branches = db.Column(db.Integer)
    num_employees = db.Column(db.Integer)
    title = db.Column(db.String(200))
    description = db.Column(db.String(300))
    foundation = db.relationship("Foundation", cascade="all,delete", backref='aboutus', lazy='dynamic')
    equipment = db.relationship("Equipment", cascade="all,delete", backref='aboutus', lazy='dynamic')
    employees = db.relationship("Employees", cascade="all,delete", backref='aboutus', lazy='dynamic')
    awards = db.relationship("Awards", cascade="all,delete", backref='aboutus', lazy='dynamic')
    partners = db.relationship("Partners", cascade="all,delete", backref='aboutus', lazy='dynamic')


class Foundation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    filename = db.Column(db.String)
    aboutus_id = db.Column(db.Integer, db.ForeignKey('aboutus.id'))

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equip = db.Column(db.String)
    aboutus_id = db.Column(db.Integer, db.ForeignKey('aboutus.id'))

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    filename = db.Column(db.String)
    aboutus_id = db.Column(db.Integer, db.ForeignKey('aboutus.id'))

class Awards(db.Model): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    aboutus_id = db.Column(db.Integer, db.ForeignKey('aboutus.id'))

class Partners(db.Model): # type: ingore
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    aboutus_id = db.Column(db.Integer, db.ForeignKey('aboutus.id'))


# Клиенты

class Clients(db.Model): # type: ignore
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    site = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.utcnow)

