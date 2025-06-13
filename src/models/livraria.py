from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabela ENDERECO
class Endereco(db.Model):
    __tablename__ = 'endereco'
    id_endereco = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(60), nullable=False)
    numero = db.Column(db.SmallInteger, nullable=False)
    complemento = db.Column(db.String(25))
    cep = db.Column(db.String(8), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    
    # Relacionamentos
    clientes = db.relationship('Cliente', backref='endereco', lazy=True)
    editoras = db.relationship('Editora', backref='endereco', lazy=True)
    fornecedores = db.relationship('Fornecedor', backref='endereco', lazy=True)
    
    def to_dict(self):
        return {
            'id_endereco': self.id_endereco,
            'rua': self.rua,
            'numero': self.numero,
            'complemento': self.complemento,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado
        }

# Tabela GENERO
class Genero(db.Model):
    __tablename__ = 'genero'
    codigo = db.Column(db.String(3), primary_key=True)
    descricao = db.Column(db.String(60), nullable=False, unique=True)
    
    # Relacionamentos
    livros = db.relationship('Livro', backref='genero', lazy=True)
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'descricao': self.descricao
        }

# Tabela EDITORA
class Editora(db.Model):
    __tablename__ = 'editora'
    id_editora = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'), nullable=False)
    
    # Relacionamentos
    livros = db.relationship('Livro', backref='editora', lazy=True)
    
    def to_dict(self):
        return {
            'id_editora': self.id_editora,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'id_endereco': self.id_endereco
        }

# Tabela AUTOR
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'id_autor': self.id_autor,
            'nome': self.nome,
            'data_nasc': self.data_nasc.strftime('%Y-%m-%d'),
            'nacionalidade': self.nacionalidade
        }

# Tabela LIVRO
class Livro(db.Model):
    __tablename__ = 'livro'
    id_livro = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    titulo = db.Column(db.String(100), nullable=False)
    ano_publicacao = db.Column(db.SmallInteger, nullable=False)
    preco_venda_padrao = db.Column(db.Numeric(6, 2), nullable=False)
    id_editora = db.Column(db.Integer, db.ForeignKey('editora.id_editora'), nullable=False)
    codigo_genero = db.Column(db.String(3), db.ForeignKey('genero.codigo'), nullable=False)
    
    # Relacionamentos
    autores = db.relationship('Autor', secondary='livro_autor', backref=db.backref('livros', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id_livro': self.id_livro,
            'isbn': self.isbn,
            'titulo': self.titulo,
            'ano_publicacao': self.ano_publicacao,
            'preco_venda_padrao': float(self.preco_venda_padrao),
            'id_editora': self.id_editora,
            'codigo_genero': self.codigo_genero
        }

# Tabela LIVRO_AUTOR (Associativa)
livro_autor = db.Table('livro_autor',
    db.Column('id_livro', db.Integer, db.ForeignKey('livro.id_livro'), primary_key=True),
    db.Column('id_autor', db.Integer, db.ForeignKey('autor.id_autor'), primary_key=True)
)

# Tabela CLIENTE
class Cliente(db.Model):
    __tablename__ = 'cliente'
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'), nullable=False)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='cliente', lazy=True)
    
    def to_dict(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'id_endereco': self.id_endereco
        }

# Tabela FORNECEDOR
class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    cnpj = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'), nullable=False)
    
    # Relacionamentos
    compras = db.relationship('Compra', backref='fornecedor', lazy=True)
    
    def to_dict(self):
        return {
            'cnpj': self.cnpj,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'id_endereco': self.id_endereco
        }

# Tabela COMPRA
class Compra(db.Model):
    __tablename__ = 'compra'
    id_compra = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date, nullable=False)
    cnpj_fornecedor = db.Column(db.String(14), db.ForeignKey('fornecedor.cnpj'), nullable=False)
    valor_total = db.Column(db.Numeric(8, 2), nullable=False)
    
    def to_dict(self):
        return {
            'id_compra': self.id_compra,
            'data_compra': self.data_compra.strftime('%Y-%m-%d'),
            'cnpj_fornecedor': self.cnpj_fornecedor,
            'valor_total': float(self.valor_total)
        }

# Tabela VENDA
class Venda(db.Model):
    __tablename__ = 'venda'
    id_venda = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.Date, nullable=False)
    cpf_cliente = db.Column(db.String(11), db.ForeignKey('cliente.cpf'), nullable=False)
    valor_total = db.Column(db.Numeric(8, 2), nullable=False)
    
    def to_dict(self):
        return {
            'id_venda': self.id_venda,
            'data_venda': self.data_venda.strftime('%Y-%m-%d'),
            'cpf_cliente': self.cpf_cliente,
            'valor_total': float(self.valor_total)
        }

# Tabela ITEM_COMPRA
class ItemCompra(db.Model):
    __tablename__ = 'item_compra'
    id_compra = db.Column(db.Integer, db.ForeignKey('compra.id_compra'), primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livro.id_livro'), primary_key=True)
    quantidade_compra = db.Column(db.SmallInteger, nullable=False)
    valor_unitario_compra = db.Column(db.Numeric(6, 2), nullable=False)
    
    # Relacionamentos
    compra = db.relationship('Compra', backref=db.backref('itens', lazy=True))
    livro = db.relationship('Livro')
    
    def to_dict(self):
        return {
            'id_compra': self.id_compra,
            'id_livro': self.id_livro,
            'quantidade_compra': self.quantidade_compra,
            'valor_unitario_compra': float(self.valor_unitario_compra)
        }

# Tabela ITEM_VENDA
class ItemVenda(db.Model):
    __tablename__ = 'item_venda'
    id_venda = db.Column(db.Integer, db.ForeignKey('venda.id_venda'), primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livro.id_livro'), primary_key=True)
    quantidade_venda = db.Column(db.SmallInteger, nullable=False)
    valor_unitario_venda = db.Column(db.Numeric(6, 2), nullable=False)
    
    # Relacionamentos
    venda = db.relationship('Venda', backref=db.backref('itens', lazy=True))
    livro = db.relationship('Livro')
    
    def to_dict(self):
        return {
            'id_venda': self.id_venda,
            'id_livro': self.id_livro,
            'quantidade_venda': self.quantidade_venda,
            'valor_unitario_venda': float(self.valor_unitario_venda)
        }

