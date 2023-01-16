# find-user-aws
Script in python to find a USER and it's key on AWS in mutiple accounts

O script está em fase de desenvolvimento ainda.

Já há funcionalidade, para executá-lo basta colocar todas os profiles para busca no arquivo .aws/credentials.

Após isso, basta passar a Access Key como argumento.

O script irá buscar o usuário com essa Access Key e criar um novo com o prefixo new- 

Ex:

python3 keysearch.py AKIA4Y5IEKUG4STAH25Q