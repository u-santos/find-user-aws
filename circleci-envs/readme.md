## Criação de váriáveis de ambiente no CircleCI via script

Script criado e desenvolvido por Juan Pablo

Este script foi feito para automatizar o processo de inserção de variáveis de ambiente dos projetos, via API do CircleCI.

## Como executar

### Token pessoal

Para executar o script, é preciso gerar um 'personal token' no CircleCI, que vai ser utilizado para autorização das operações feitas.
Para isto, basta acessar o perfil pessoal >> Personal API Tokens >> Create New Token (se já não possuir um).

Este token deverá ser atribuído à variável CIRCLE_PERSONAL_TOKEN, no arquivo config.yml, assim como o nome do repositório do projeto o qual terá as variáveis de ambiente inseridas.

### Instalação das dependências

Deve-se utilizar o Python 3.8 para execução do script.
A única dependência necessária para instalação, utilizando o pip, é o pyyaml.
Portanto, basta que faça o seguinte comando no terminal:

```
pip install pyyaml

```

Ou faça uso do requirements.txt:

```
pip install -r requirements.txt
```

## Execução do Script

Para executar, basta somente que tenha o arquivo config.yml e o arquivo contendo as variáveis e seus respectivos valores configurados propriamente (assim como o exemplo deixado, contendo sempre NOME=VALOR da variável), e executar o seguinte comando no terminal, dentro da pasta onde está o script:

```
python3 circleci_create_envs.py
```

