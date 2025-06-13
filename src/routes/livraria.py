from flask import Blueprint, jsonify, request
from src.models.livraria import db, Endereco, Genero, Editora, Autor, Livro, Cliente, Fornecedor, Compra, Venda, ItemCompra, ItemVenda
from sqlalchemy import func
from datetime import datetime

livraria_bp = Blueprint('livraria', __name__)

# Rotas para GENERO
@livraria_bp.route('/generos', methods=['GET'])
def get_generos():
    generos = Genero.query.all()
    return jsonify([genero.to_dict() for genero in generos])

@livraria_bp.route('/generos', methods=['POST'])
def create_genero():
    data = request.json
    genero = Genero(codigo=data['codigo'], descricao=data['descricao'])
    db.session.add(genero)
    db.session.commit()
    return jsonify(genero.to_dict()), 201

@livraria_bp.route('/generos/<codigo>', methods=['GET'])
def get_genero(codigo):
    genero = Genero.query.get_or_404(codigo)
    return jsonify(genero.to_dict())

@livraria_bp.route('/generos/<codigo>', methods=['PUT'])
def update_genero(codigo):
    genero = Genero.query.get_or_404(codigo)
    data = request.json
    genero.descricao = data.get('descricao', genero.descricao)
    db.session.commit()
    return jsonify(genero.to_dict())

@livraria_bp.route('/generos/<codigo>', methods=['DELETE'])
def delete_genero(codigo):
    genero = Genero.query.get_or_404(codigo)
    db.session.delete(genero)
    db.session.commit()
    return '', 204

# Rotas para LIVRO
@livraria_bp.route('/livros', methods=['GET'])
def get_livros():
    livros = Livro.query.all()
    result = []
    for livro in livros:
        livro_dict = livro.to_dict()
        livro_dict['editora'] = livro.editora.nome
        livro_dict['genero'] = livro.genero.descricao
        livro_dict['autores'] = [autor.nome for autor in livro.autores]
        result.append(livro_dict)
    return jsonify(result)

@livraria_bp.route('/livros', methods=['POST'])
def create_livro():
    data = request.json
    livro = Livro(
        isbn=data['isbn'],
        titulo=data['titulo'],
        ano_publicacao=data['ano_publicacao'],
        preco_venda_padrao=data['preco_venda_padrao'],
        id_editora=data['id_editora'],
        codigo_genero=data['codigo_genero']
    )
    db.session.add(livro)
    db.session.commit()
    
    # Adicionar autores se fornecidos
    if 'autores' in data:
        for autor_id in data['autores']:
            autor = Autor.query.get(autor_id)
            if autor:
                livro.autores.append(autor)
        db.session.commit()
    
    return jsonify(livro.to_dict()), 201

@livraria_bp.route('/livros/<int:id_livro>', methods=['GET'])
def get_livro(id_livro):
    livro = Livro.query.get_or_404(id_livro)
    livro_dict = livro.to_dict()
    livro_dict['editora'] = livro.editora.nome
    livro_dict['genero'] = livro.genero.descricao
    livro_dict['autores'] = [autor.nome for autor in livro.autores]
    return jsonify(livro_dict)

@livraria_bp.route('/livros/<int:id_livro>', methods=['PUT'])
def update_livro(id_livro):
    livro = Livro.query.get_or_404(id_livro)
    data = request.json
    
    livro.isbn = data.get('isbn', livro.isbn)
    livro.titulo = data.get('titulo', livro.titulo)
    livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
    livro.preco_venda_padrao = data.get('preco_venda_padrao', livro.preco_venda_padrao)
    livro.id_editora = data.get('id_editora', livro.id_editora)
    livro.codigo_genero = data.get('codigo_genero', livro.codigo_genero)
    
    # Atualizar autores se fornecidos
    if 'autores' in data:
        livro.autores = []
        for autor_id in data['autores']:
            autor = Autor.query.get(autor_id)
            if autor:
                livro.autores.append(autor)
    
    db.session.commit()
    return jsonify(livro.to_dict())

@livraria_bp.route('/livros/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    livro = Livro.query.get_or_404(id_livro)
    db.session.delete(livro)
    db.session.commit()
    return '', 204

# Rotas para CLIENTE
@livraria_bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    result = []
    for cliente in clientes:
        cliente_dict = cliente.to_dict()
        cliente_dict['endereco'] = cliente.endereco.to_dict()
        result.append(cliente_dict)
    return jsonify(result)

@livraria_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    
    # Criar endereço primeiro se fornecido
    endereco_id = data.get('id_endereco')
    if not endereco_id and 'endereco' in data:
        endereco_data = data['endereco']
        endereco = Endereco(
            rua=endereco_data['rua'],
            numero=endereco_data['numero'],
            complemento=endereco_data.get('complemento'),
            cep=endereco_data['cep'],
            cidade=endereco_data['cidade'],
            estado=endereco_data['estado']
        )
        db.session.add(endereco)
        db.session.flush()  # Para obter o ID sem commit
        endereco_id = endereco.id_endereco
    
    cliente = Cliente(
        cpf=data['cpf'],
        nome=data['nome'],
        telefone=data.get('telefone'),
        email=data['email'],
        id_endereco=endereco_id
    )
    db.session.add(cliente)
    db.session.commit()
    
    cliente_dict = cliente.to_dict()
    cliente_dict['endereco'] = cliente.endereco.to_dict()
    return jsonify(cliente_dict), 201

# Rota para ESTOQUE (Relatório)
@livraria_bp.route('/relatorios/estoque', methods=['GET'])
def get_estoque():
    # Subconsulta para calcular total de compras por livro
    compras_subquery = db.session.query(
        ItemCompra.id_livro,
        func.sum(ItemCompra.quantidade_compra).label('total_comprado')
    ).group_by(ItemCompra.id_livro).subquery()
    
    # Subconsulta para calcular total de vendas por livro
    vendas_subquery = db.session.query(
        ItemVenda.id_livro,
        func.sum(ItemVenda.quantidade_venda).label('total_vendido')
    ).group_by(ItemVenda.id_livro).subquery()
    
    # Consulta principal juntando livros, compras e vendas
    result = db.session.query(
        Livro.id_livro,
        Livro.titulo,
        Livro.isbn,
        func.coalesce(compras_subquery.c.total_comprado, 0).label('total_comprado'),
        func.coalesce(vendas_subquery.c.total_vendido, 0).label('total_vendido'),
        (func.coalesce(compras_subquery.c.total_comprado, 0) - func.coalesce(vendas_subquery.c.total_vendido, 0)).label('estoque_atual')
    ).outerjoin(
        compras_subquery, Livro.id_livro == compras_subquery.c.id_livro
    ).outerjoin(
        vendas_subquery, Livro.id_livro == vendas_subquery.c.id_livro
    ).all()
    
    estoque_list = []
    for item in result:
        estoque_list.append({
            'id_livro': item.id_livro,
            'titulo': item.titulo,
            'isbn': item.isbn,
            'total_comprado': item.total_comprado,
            'total_vendido': item.total_vendido,
            'estoque_atual': item.estoque_atual
        })
    
    return jsonify(estoque_list)

# Rota para VENDAS (Relatório)
@livraria_bp.route('/relatorios/vendas', methods=['GET'])
def get_vendas_relatorio():
    vendas = Venda.query.all()
    result = []
    
    for venda in vendas:
        venda_dict = venda.to_dict()
        venda_dict['cliente'] = venda.cliente.nome
        
        itens = []
        for item in venda.itens:
            item_dict = item.to_dict()
            item_dict['livro'] = item.livro.titulo
            item_dict['subtotal'] = float(item.quantidade_venda * item.valor_unitario_venda)
            itens.append(item_dict)
        
        venda_dict['itens'] = itens
        result.append(venda_dict)
    
    return jsonify(result)

# Rota para LIVROS MAIS VENDIDOS (Relatório)
@livraria_bp.route('/relatorios/livros-mais-vendidos', methods=['GET'])
def get_livros_mais_vendidos():
    result = db.session.query(
        Livro.id_livro,
        Livro.titulo,
        Livro.isbn,
        func.sum(ItemVenda.quantidade_venda).label('total_vendido')
    ).join(
        ItemVenda, Livro.id_livro == ItemVenda.id_livro
    ).group_by(
        Livro.id_livro, Livro.titulo, Livro.isbn
    ).order_by(
        func.sum(ItemVenda.quantidade_venda).desc()
    ).limit(5).all()
    
    livros_list = []
    for item in result:
        livros_list.append({
            'id_livro': item.id_livro,
            'titulo': item.titulo,
            'isbn': item.isbn,
            'total_vendido': item.total_vendido
        })
    
    return jsonify(livros_list)

