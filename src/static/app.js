// Script principal para o Sistema de Controle de Vendas de Livraria

document.addEventListener('DOMContentLoaded', function() {
    // Navegação entre páginas
    setupNavigation();
    
    // Carregar dados iniciais
    loadLivros();
    loadClientes();
    loadVendas();
    loadRelatorios();
    
    // Setup de eventos
    setupEventListeners();
});

// Configuração da navegação entre páginas
function setupNavigation() {
    // Links da navbar
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetPage = this.getAttribute('data-page');
            showPage(targetPage);
        });
    });
    
    // Botões de navegação nos cards
    document.querySelectorAll('[data-navigate]').forEach(button => {
        button.addEventListener('click', function() {
            const targetPage = this.getAttribute('data-navigate');
            showPage(targetPage);
        });
    });
}

// Mostrar página específica
function showPage(pageId) {
    // Esconder todas as páginas
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Mostrar a página selecionada
    document.getElementById(pageId).classList.add('active');
    
    // Atualizar links ativos
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === pageId) {
            link.classList.add('active');
        }
    });
}

// Configuração de eventos
function setupEventListeners() {
    // Botão Novo Livro
    document.getElementById('btnNovoLivro').addEventListener('click', function() {
        document.getElementById('livroModalLabel').textContent = 'Novo Livro';
        document.getElementById('livroForm').reset();
        const livroModal = new bootstrap.Modal(document.getElementById('livroModal'));
        livroModal.show();
    });
    
    // Botão Salvar Livro
    document.getElementById('salvarLivro').addEventListener('click', function() {
        // Implementar lógica para salvar livro
        const livroModal = bootstrap.Modal.getInstance(document.getElementById('livroModal'));
        livroModal.hide();
        
        // Recarregar lista de livros após salvar
        loadLivros();
    });
    
    // Filtrar vendas por período
    document.getElementById('filtrarVendas').addEventListener('click', function() {
        const dataInicio = document.getElementById('dataInicio').value;
        const dataFim = document.getElementById('dataFim').value;
        
        // Implementar lógica para filtrar vendas por período
        console.log(`Filtrar vendas de ${dataInicio} até ${dataFim}`);
    });
}

// Carregar dados de livros
function loadLivros() {
    // Simulação de dados para demonstração
    const livros = [
        { isbn: '9788535902778', titulo: 'Dom Casmurro', ano: 1899, genero: 'Romance', editora: 'Editora Alfa', preco: 35.00 },
        { isbn: '9788532510612', titulo: 'A Hora da Estrela', ano: 1977, genero: 'Ficção', editora: 'Editora Beta', preco: 28.50 },
        { isbn: '9788525044641', titulo: 'E Não Sobrou Nenhum', ano: 1939, genero: 'Suspense', editora: 'Editora Gama', preco: 45.00 },
        { isbn: '9788576570052', titulo: 'Eu, Robô', ano: 1950, genero: 'Ciência', editora: 'Editora Alfa', preco: 39.90 },
        { isbn: '9788572328002', titulo: 'Frankenstein', ano: 1818, genero: 'Ficção', editora: 'Editora Beta', preco: 32.00 }
    ];
    
    const tableBody = document.getElementById('livrosTableBody');
    tableBody.innerHTML = '';
    
    livros.forEach(livro => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${livro.isbn}</td>
            <td>${livro.titulo}</td>
            <td>${livro.ano}</td>
            <td>${livro.genero}</td>
            <td>${livro.editora}</td>
            <td>R$ ${livro.preco.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
                <button class="btn btn-sm btn-info btn-action" title="Detalhes">
                    <i class="bi bi-info-circle"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
    
    // Preencher selects de gêneros e editoras
    const generos = ['Romance', 'Ficção', 'Suspense', 'Ciência', 'História'];
    const selectGenero = document.getElementById('genero');
    selectGenero.innerHTML = '<option value="">Selecione um gênero</option>';
    generos.forEach(genero => {
        const option = document.createElement('option');
        option.value = genero;
        option.textContent = genero;
        selectGenero.appendChild(option);
    });
    
    const editoras = ['Editora Alfa', 'Editora Beta', 'Editora Gama'];
    const selectEditora = document.getElementById('editora');
    selectEditora.innerHTML = '<option value="">Selecione uma editora</option>';
    editoras.forEach(editora => {
        const option = document.createElement('option');
        option.value = editora;
        option.textContent = editora;
        selectEditora.appendChild(option);
    });
}

// Carregar dados de clientes
function loadClientes() {
    // Simulação de dados para demonstração
    const clientes = [
        { cpf: '11122233344', nome: 'João Silva', telefone: '31999998888', email: 'joao.silva@email.com', cidade: 'Belo Horizonte', uf: 'MG' },
        { cpf: '55566677788', nome: 'Maria Oliveira', telefone: '21988887777', email: 'maria.oliveira@email.com', cidade: 'Rio de Janeiro', uf: 'RJ' },
        { cpf: '99988877766', nome: 'Pedro Souza', telefone: '11977776666', email: 'pedro.souza@email.com', cidade: 'São Paulo', uf: 'SP' }
    ];
    
    const tableBody = document.getElementById('clientesTableBody');
    tableBody.innerHTML = '';
    
    clientes.forEach(cliente => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${cliente.cpf}</td>
            <td>${cliente.nome}</td>
            <td>${cliente.telefone}</td>
            <td>${cliente.email}</td>
            <td>${cliente.cidade}/${cliente.uf}</td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
                <button class="btn btn-sm btn-info btn-action" title="Detalhes">
                    <i class="bi bi-info-circle"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Carregar dados de vendas
function loadVendas() {
    // Simulação de dados para demonstração
    const vendas = [
        { id: 1, data: '2025-03-01', cliente: 'João Silva', valor: 70.00 },
        { id: 2, data: '2025-03-05', cliente: 'Maria Oliveira', valor: 45.00 },
        { id: 3, data: '2025-03-10', cliente: 'Pedro Souza', valor: 39.90 }
    ];
    
    const tableBody = document.getElementById('vendasTableBody');
    tableBody.innerHTML = '';
    
    vendas.forEach(venda => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${venda.id}</td>
            <td>${formatDate(venda.data)}</td>
            <td>${venda.cliente}</td>
            <td>R$ ${venda.valor.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
                <button class="btn btn-sm btn-info btn-action" title="Detalhes">
                    <i class="bi bi-info-circle"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Carregar dados de relatórios
function loadRelatorios() {
    // Relatório de Estoque
    const estoqueData = [
        { isbn: '9788535902778', titulo: 'Dom Casmurro', comprados: 10, vendidos: 3, estoque: 7 },
        { isbn: '9788532510612', titulo: 'A Hora da Estrela', comprados: 15, vendidos: 8, estoque: 7 },
        { isbn: '9788525044641', titulo: 'E Não Sobrou Nenhum', comprados: 8, vendidos: 5, estoque: 3 },
        { isbn: '9788576570052', titulo: 'Eu, Robô', comprados: 12, vendidos: 6, estoque: 6 },
        { isbn: '9788572328002', titulo: 'Frankenstein', comprados: 10, vendidos: 2, estoque: 8 }
    ];
    
    const estoqueTableBody = document.getElementById('estoqueTableBody');
    estoqueTableBody.innerHTML = '';
    
    estoqueData.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.isbn}</td>
            <td>${item.titulo}</td>
            <td>${item.comprados}</td>
            <td>${item.vendidos}</td>
            <td>${item.estoque}</td>
        `;
        estoqueTableBody.appendChild(row);
    });
    
    // Gráfico de Livros Mais Vendidos
    const livrosMaisVendidosCtx = document.getElementById('livrosMaisVendidosChart').getContext('2d');
    new Chart(livrosMaisVendidosCtx, {
        type: 'bar',
        data: {
            labels: ['A Hora da Estrela', 'Eu, Robô', 'E Não Sobrou Nenhum', 'Dom Casmurro', 'Frankenstein'],
            datasets: [{
                label: 'Quantidade Vendida',
                data: [8, 6, 5, 3, 2],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
    
    // Gráfico de Vendas por Período
    const vendasPorPeriodoCtx = document.getElementById('vendasPorPeriodoChart').getContext('2d');
    new Chart(vendasPorPeriodoCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Valor Total de Vendas (R$)',
                data: [1200, 1900, 3000, 2500, 2800, 3500],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

