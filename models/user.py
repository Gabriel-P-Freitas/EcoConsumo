from extensions import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    user_type = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(255))


    __mapper_args__ = {'polymorphic_on': user_type}

    def __init__(self, name, email=None, password=None, phone=None, picture=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.picture = picture

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"


class Doador(User):
    __tablename__ = "doador"
    __mapper_args__ = {'polymorphic_identity': 'doador'}

    birth_date = db.Column(db.String(10))

    def __init__(self, name=None, email=None, password=None, birth_date=None, phone=None, picture=None):
        super().__init__(name, email, password, phone, picture)
        self.birth_date = birth_date

    def __repr__(self):
        return f"<Doador {self.name}>"

class Empresa(User):
    __tablename__ = "empresa"
    __mapper_args__ = {'polymorphic_identity': 'empresa'}

    cnpj = db.Column(db.String(14), unique=True)

    address_cep = db.Column(db.String(8))
    address_neighborhood = db.Column(db.String(100))
    address_street = db.Column(db.String(100))
    address_number = db.Column(db.String(10))

    def __init__(self, name=None, email=None, password=None, 
                 cnpj=None, phone=None, address_cep=None, 
                 address_neighborhood=None, address_street=None, 
                 address_number=None, picture=None):
        super().__init__(name, email, password, phone, picture)
        self.cnpj = cnpj
        self.address_zipcode = address_cep
        self.address_neighborhood = address_neighborhood
        self.address_street = address_street
        self.address_number = address_number

    def __repr__(self):
        return f"<Empresa {self.name}>"

class Admin(User):
    __tablename__ = "admin"
    __mapper_args__ = {'polymorphic_identity': 'Admin'}

    access_level = db.Column(db.Integer, default=1)

    def __init__(self, name, email, password, access_level=1):
        super().__init__(name, email, password)
        self.access_level = access_level

    def __repr__(self):
        return f"<Admin {self.name}>"

