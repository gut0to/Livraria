from flask import Blueprint, jsonify, request
from src.models.livraria import db, Genero, Livro, Autor, Cliente, Venda, ItemCompra, ItemVenda
from sqlalchemy import func, text
from datetime import datetime

livraria_bp = Blueprint('livraria', __name__)

# ====================================================================
# Rotas para GENERO
# ====================================================================

@livraria_bp.route('/generos', methods=['GET'])
def get_generos():
    generos = Genero.query.all()
    return jsonify([genero.to_dict() for genero in generos])

@livraria_bp.route('/generos', methods=['POST'])
def create_genero():
    data = request.json
    sql = text("INSERT INTO genero (codigo, descricao) VALUES (:codigo, :descricao)")
    try:
        db.session.execute(sql, {"codigo": data['codigo'], "descricao": data['descricao']})
        db.session.commit()
        return jsonify(data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar gênero: {str(e)}"}), 500

@livraria_bp.route('/generos/<codigo>', methods=['GET'])
def get_genero(codigo):
    
    genero = Genero.query.get_or_404(codigo)
    return jsonify(genero.to_dict())

@livraria_bp.route('/generos/<codigo>', methods=['PUT'])
def update_genero(codigo):
    data = request.json
    sql = text("UPDATE genero SET descricao = :descricao WHERE codigo = :codigo")
    try:
        result = db.session.execute(sql, {"descricao": data.get('descricao'), "codigo": codigo})
        if result.rowcount == 0:
            return jsonify({"error": "Gênero não encontrado."}), 404
        db.session.commit()
        return jsonify({"message": "Gênero atualizado com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar gênero: {str(e)}"}), 500

@livraria_bp.route('/generos/<codigo>', methods=['DELETE'])
def delete_genero(codigo):
    sql = text("DELETE FROM genero WHERE codigo = :codigo")
    try:
        result = db.session.execute(sql, {"codigo": codigo})
        if result.rowcount == 0:
            return jsonify({"error": "Gênero não encontrado."}), 404
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar gênero: {str(e)}"}), 500

# ====================================================================
# Rotas para LIVRO
# ====================================================================

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
    sql_livro = text("""
        INSERT INTO livro (isbn, titulo, ano_publicacao, preco_venda_padrao, id_editora, codigo_genero) 
        VALUES (:isbn, :titulo, :ano, :preco, :id_editora, :cod_genero)
        RETURNING id_livro
    """)
    sql_livro_autor = text("INSERT INTO livro_autor (id_livro, id_autor) VALUES (:id_livro, :id_autor)")
    
    try:
        result = db.session.execute(sql_livro, {
            "isbn": data['isbn'], "titulo": data['titulo'], "ano": data['ano_publicacao'],
            "preco": data['preco_venda_padrao'], "id_editora": data['id_editora'], "cod_genero": data['codigo_genero']
        })
        new_livro_id = result.scalar_one()

        if 'autores' in data:
            for autor_id in data['autores']:
                db.session.execute(sql_livro_autor, {"id_livro": new_livro_id, "id_autor": autor_id})
        
        db.session.commit()
        livro_criado = Livro.query.get(new_livro_id) 
        return jsonify(livro_criado.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar livro: {str(e)}"}), 500

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
    data = request.json
    sql_update_livro = text("""
        UPDATE livro SET isbn = :isbn, titulo = :titulo, ano_publicacao = :ano, 
        preco_venda_padrao = :preco, id_editora = :id_editora, codigo_genero = :cod_genero
        WHERE id_livro = :id_livro
    """)
    sql_delete_autores = text("DELETE FROM livro_autor WHERE id_livro = :id_livro")
    sql_insert_autor = text("INSERT INTO livro_autor (id_livro, id_autor) VALUES (:id_livro, :id_autor)")

    try:
        db.session.execute(sql_update_livro, {**data, "id_livro": id_livro})

        if 'autores' in data:
            db.session.execute(sql_delete_autores, {"id_livro": id_livro})
            for autor_id in data['autores']:
                db.session.execute(sql_insert_autor, {"id_livro": id_livro, "id_autor": autor_id})
        
        db.session.commit()
        return jsonify({"message": "Livro atualizado com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar livro: {str(e)}"}), 500

@livraria_bp.route('/livros/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    
    sql_del_item_venda = text("DELETE FROM item_venda WHERE id_livro = :id_livro")
    sql_del_item_compra = text("DELETE FROM item_compra WHERE id_livro = :id_livro")
    sql_del_livro_autor = text("DELETE FROM livro_autor WHERE id_livro = :id_livro")
    sql_del_livro = text("DELETE FROM livro WHERE id_livro = :id_livro")
    try:
        db.session.execute(sql_del_item_venda, {"id_livro": id_livro})
        db.session.execute(sql_del_item_compra, {"id_livro": id_livro})
        db.session.execute(sql_del_livro_autor, {"id_livro": id_livro})
        result = db.session.execute(sql_del_livro, {"id_livro": id_livro})

        if result.rowcount == 0:
            return jsonify({"error": "Livro não encontrado."}), 404

        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar livro: {str(e)}"}), 500

# ====================================================================
# Rotas para CLIENTE
# ====================================================================

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
    sql_insert_endereco = text("""
        INSERT INTO endereco (rua, numero, complemento, cep, cidade, estado)
        VALUES (:rua, :numero, :complemento, :cep, :cidade, :estado) RETURNING id_endereco
    """)
    sql_insert_cliente = text("""
        INSERT INTO cliente (cpf, nome, telefone, email, id_endereco)
        VALUES (:cpf, :nome, :telefone, :email, :id_endereco)
    """)
    try:
        endereco_id = data.get('id_endereco')
        if not endereco_id and 'endereco' in data:
            endereco_data = data['endereco']
            result = db.session.execute(sql_insert_endereco, endereco_data)
            endereco_id = result.scalar_one()

        db.session.execute(sql_insert_cliente, {
            "cpf": data['cpf'], "nome": data['nome'], "telefone": data.get('telefone'),
            "email": data['email'], "id_endereco": endereco_id
        })
        db.session.commit()
        return jsonify({"message": "Cliente criado com sucesso."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao criar cliente: {str(e)}"}), 500


# ====================================================================
# Rotas para RELATÓRIOS 
# ====================================================================

@livraria_bp.route('/relatorios/estoque', methods=['GET'])
def get_estoque():
    compras_subquery = db.session.query(ItemCompra.id_livro, func.sum(ItemCompra.quantidade_compra).label('total_comprado')).group_by(ItemCompra.id_livro).subquery()
    vendas_subquery = db.session.query(ItemVenda.id_livro, func.sum(ItemVenda.quantidade_venda).label('total_vendido')).group_by(ItemVenda.id_livro).subquery()
    
    result = db.session.query(
        Livro.id_livro, Livro.titulo, Livro.isbn,
        func.coalesce(compras_subquery.c.total_comprado, 0).label('total_comprado'),
        func.coalesce(vendas_subquery.c.total_vendido, 0).label('total_vendido'),
        (func.coalesce(compras_subquery.c.total_comprado, 0) - func.coalesce(vendas_subquery.c.total_vendido, 0)).label('estoque_atual')
    ).outerjoin(compras_subquery, Livro.id_livro == compras_subquery.c.id_livro).outerjoin(vendas_subquery, Livro.id_livro == vendas_subquery.c.id_livro).all()
    
    return jsonify([{
        'id_livro': item.id_livro, 'titulo': item.titulo, 'isbn': item.isbn,
        'total_comprado': item.total_comprado, 'total_vendido': item.total_vendido, 'estoque_atual': item.estoque_atual
    } for item in result])

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

@livraria_bp.route('/relatorios/livros-mais-vendidos', methods=['GET'])
def get_livros_mais_vendidos():
    result = db.session.query(
        Livro.id_livro, Livro.titulo, Livro.isbn, func.sum(ItemVenda.quantidade_venda).label('total_vendido')
    ).join(ItemVenda, Livro.id_livro == ItemVenda.id_livro).group_by(
        Livro.id_livro, Livro.titulo, Livro.isbn
    ).order_by(func.sum(ItemVenda.quantidade_venda).desc()).limit(5).all()
    
    return jsonify([{
        'id_livro': item.id_livro, 'titulo': item.titulo, 'isbn': item.isbn, 'total_vendido': item.total_vendido
    } for item in result])