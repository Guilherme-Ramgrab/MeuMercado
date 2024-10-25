import json

ARQUIVO_DADOS = "produtos.json"
SENHA_ADMIN = "1234"  # Defina a senha para operações administrativas

# Função para carregar dados do arquivo JSON
def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r") as file:
            dados = json.load(file)
            if "produtos" not in dados:
                dados["produtos"] = []
            return dados
    except FileNotFoundError:
        dados_iniciais = {"produtos": []}
        salvar_dados(dados_iniciais)
        return dados_iniciais
    except json.JSONDecodeError:
        return {"produtos": []}

# Função para salvar dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as file:
        json.dump(dados, file, indent=4)

# Função para verificar senha
def verificar_senha():
    senha = input("Digite a senha de administrador: ")
    return senha == SENHA_ADMIN

# Função para validar entrada de números inteiros (para código e quantidade)
def obter_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro válido.")

# Função para validar entrada de números (para valor de venda)
def obter_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um valor numérico válido.")

# Função para verificar se o código já existe
def codigo_existe(codigo, produtos):
    for produto in produtos:
        if produto["codigo"] == codigo:
            return True
    return False

# F004: Cadastrar produtos com validação de entrada
def cadastrar_produto():
    if not verificar_senha():
        print("Senha incorreta!")
        return

    dados = carregar_dados()
    produtos = dados["produtos"]

    # Solicitar código até que seja fornecido um código que não exista
    while True:
        codigo = obter_inteiro("Código do produto: ")
        if codigo_existe(codigo, produtos):
            print("Código existente! Por favor, insira um novo código.")
        else:
            break
    
    # Validar nome e tipo do produto
    while True:
        nome = input("Nome do produto: ").strip()
        if nome == "":
            print("Entrada inválida! O nome não pode estar vazio.")
        else:
            break

    while True:
        tipo = input("Tipo do produto: ").strip()
        if tipo == "":
            print("Entrada inválida! O tipo não pode estar vazio.")
        else:
            break

    valor = obter_float("Valor de venda: ")
    quantidade = obter_inteiro("Quantidade em estoque: ")

    produtos.append({
        "codigo": codigo,
        "nome": nome,
        "tipo": tipo,
        "valor": valor,
        "quantidade": quantidade
    })
    salvar_dados(dados)
    print("Produto cadastrado com sucesso!")

# F005: Excluir produto
def excluir_produto():
    if not verificar_senha():
        print("Senha incorreta!")
        return
    codigo = obter_inteiro("Código do produto a excluir: ")
    dados = carregar_dados()
    produtos = dados["produtos"]
    produtos = [p for p in produtos if p["codigo"] != codigo]
    dados["produtos"] = produtos
    salvar_dados(dados)
    print("Produto excluído com sucesso!")

# F006: Alterar valor de produto
def alterar_valor_produto():
    if not verificar_senha():
        print("Senha incorreta!")
        return
    codigo = obter_inteiro("Código do produto: ")

    dados = carregar_dados()
    produtos = dados["produtos"]
    for produto in produtos:
        if produto["codigo"] == codigo:
            produto["valor"] = obter_float("Novo valor de venda: ")
            break
    else:
        print("Produto não encontrado!")
        return

    salvar_dados(dados)
    print("Valor do produto alterado com sucesso!")

# F007: Alterar estoque de produto
def alterar_estoque_produto():
    if not verificar_senha():
        print("Senha incorreta!")
        return
    codigo = obter_inteiro("Código do produto: ")

    dados = carregar_dados()
    produtos = dados["produtos"]
    for produto in produtos:
        if produto["codigo"] == codigo:
            produto["quantidade"] = obter_inteiro("Nova quantidade em estoque: ")
            break
    else:
        print("Produto não encontrado!")
        return

    salvar_dados(dados)
    print("Estoque do produto alterado com sucesso!")

# F001: Listar produtos
def listar_produtos():
    dados = carregar_dados()
    produtos = dados["produtos"]
    print("--------- ESTOQUE ---------")
    print("CODIGO | NOME | TIPO | VALOR | ESTOQUE")
    for produto in produtos:
        print(f'{produto['codigo']} | {produto['nome']} | {produto["tipo"]} | {produto["valor"]} | {produto["quantidade"]}')

# F002: Busca de produtos por nome com tratamento de lista vazia
def buscar_produto_por_nome():
    dados = carregar_dados()
    while True:
        nome = input("Digite o nome do produto: ").strip()
        if nome == "":
            print("Entrada inválida! Informe o nome.")
        else:
            produtos = dados["produtos"]
            resultados = [p for p in produtos if nome.lower() in p["nome"].lower()]
            if resultados:
                print("CODIGO | NOME | TIPO | VALOR | ESTOQUE")
                for produto in resultados:
                    print(f'{produto['codigo']} | {produto['nome']} | {produto["tipo"]} | {produto["valor"]} | {produto["quantidade"]}')
                break
            else:
                print("Nenhum produto encontrado. Tente novamente.")

# F003: Busca de produtos por tipo com tratamento de lista vazia
def buscar_produto_por_tipo():
    dados = carregar_dados()
    while True:
        tipo = input("Digite o tipo do produto: ").strip()
        if tipo == "":
            print("Entrada inválida! Informe o tipo.")
        else:
            produtos = dados["produtos"]
            resultados = [p for p in produtos if tipo.lower() in p["tipo"].lower()]
            if resultados:
                print("CODIGO | NOME | TIPO | VALOR | ESTOQUE")
                for produto in resultados:
                    print(f'{produto['codigo']} | {produto['nome']} | {produto["tipo"]} | {produto["valor"]} | {produto["quantidade"]}')
                break
            else:
                print("Nenhum produto encontrado. Tente novamente.")

# Menu principal
def menu():
    while True:
        print("\nMenu de opções:")
        print("1 - Listar produtos")
        print("2 - Buscar produto por nome")
        print("3 - Buscar produto por tipo")
        print("4 - Cadastrar produto")
        print("5 - Excluir produto")
        print("6 - Alterar valor de produto")
        print("7 - Alterar estoque de produto")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            buscar_produto_por_nome()
        elif opcao == "3":
            buscar_produto_por_tipo()
        elif opcao == "4":
            cadastrar_produto()
        elif opcao == "5":
            excluir_produto()
        elif opcao == "6":
            alterar_valor_produto()
        elif opcao == "7":
            alterar_estoque_produto()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# Execução do programa
if __name__ == "__main__":
    menu()
