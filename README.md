Modo de utilização

1 - Crie um diretório e faça o download do script e do arquivo de configuração.

mkdir /scripts

mkdir /scripts/exportados

cd /scripts

wget https://raw.githubusercontent.com/mvldebian/exporta-contatos-roundcube/main/config.json

wget https://raw.githubusercontent.com/mvldebian/exporta-contatos-roundcube/main/exporta-contatos.py

chmod +x exporta-contatos.py

2 - Edite as informações de conexão com o banco no arquivo config.json

3 - Instale as dependências do script

apt-get install python3-pip
pip3 install mysql-connector

4 - Execute o script e acompanhe a saída no console

./exporta-contatos.py

5 - Extra, o Roundcube possui um plugin chamado automatic_addressbook que coleta automaticamente contatos
Para exportar também estes contatos coletados, basta mudar no script a linha abaixo:

De: query = ("SELECT email, vcard, words, del FROM contacts WHERE user_id = %s")
Para: query = ("SELECT email, vcard, words, del FROM collected_contacts WHERE user_id = %s")
