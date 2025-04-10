# Coleta de Dados de Sensores

Este projeto tem como objetivo a coleta de dados de sensores a partir da API especificada e a conciliação dessas informações com a base de dados do middleware.

## Requisitos

Antes de iniciar, certifique-se de que o gerenciador de pacotes `uv` está instalado. Caso não esteja, utilize o seguinte comando para instalá-lo:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalação de Dependências

A instalação das dependências é necessária apenas na primeira execução ou quando houver alterações nas mesmas.

```bash
uv sync
```

## Configuração do Ambiente

Antes de executar o projeto pela primeira vez, crie o arquivo de variáveis de ambiente:

```bash
cp .env_sample .env
```

## Execução dos Módulos

### Coletar Dados da API CMA_WEB

Para coletar as informações da API CMA_WEB, execute:

```bash
PYTHONPATH=$(pwd) uv run python -m app.collect_cma_web
```

### Apagar a Base de Dados
Para apagar a base de dados, utilize o seguinte comando:

```bash
$ ./reset_db.sh 
Iniciando migrações em ../CMA_Gateway.db
Executing migration: 0001_initial_db.py
Executing migration: 0002_add_field.py
Executing migration: 0003_remove_marca_modelo.py
Migration file 0003_remove_marca_modelo.py does not contain a run_migration function.
Database reset complete.
```

### Migrate - Para atualizar um Banco de Dados existente para versão mais recente
Para atualizar um banco de dados existente para a versão mais recente, utilize o seguinte comando:
- Só atualiza se houver alterações para ser aplicada.

```bash
$ uv run python -m app.migrate
```

### Conciliação das Informações com o Middleware
Para reconciliar as informações coletadas com as bases de dados do `CMA_Gateway` e `ScadaLTS`, utilize o comando:

```bash
PYTHONPATH=$(pwd) uv run python -m app.reconcile2.main
```

Caso seja necessário conciliar individualmente com cada base de dados, utilize os comandos abaixo:

- Para reconciliar com o `ScadaLTS`:

  ```bash
  PYTHONPATH=$(pwd) uv run python -m app.reconcile.scadalts
  ```

- Para reconciliar com o `CMA_Gateway_DB`:

  ```bash
  PYTHONPATH=$(pwd) uv run python -m app.reconcile.cma_gateway_db
  ```

## Obtenção de Token de Autenticação

Embora não seja um passo obrigatório, o seguinte comando pode ser utilizado para facilitar a obtenção do token de autenticação:

```bash
PYTHONPATH=$(pwd) uv run python app/login.py
```

## Execução dos Testes

Para rodar a suíte de testes do projeto, utilize:

```bash
PYTHONPATH=$(pwd) uv run python tests/test.py
```
