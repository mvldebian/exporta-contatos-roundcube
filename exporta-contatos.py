#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

Script de exportação dos contatos do Roundcube Webmail
Exporta todos os contatos de todas as contas de e-mails ativas no banco de dados para o formato vcard.
Antes de executar instale as dependências:

apt-get install python3-pip
pip3 install mysql-connector

"""

import argparse
import codecs
import json
import mysql.connector
import os
import os.path
from collections import namedtuple


DEFAULT_CONFIG = "./config.json"
DEFAULT_OUT = "./exportados"

User = namedtuple("User", ["id", "email"])
Contact = namedtuple("Contact", ["email", "vcard", "words", "deleted"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="json config", default=DEFAULT_CONFIG)
    parser.add_argument("--out", help="output directory path", default=DEFAULT_OUT)
    return parser.parse_args()


def load_config(path):
    with open(path, "r") as fobj:
        config = json.load(fobj)
    return config


def get_users(mysql_cnx):

"""

Pega todos os IDS de usuários em 'user_id' e 'username' da tabela 'users'.

"""

    mysql_cur = mysql_cnx.cursor()
    query = ("SELECT user_id, username FROM users")

    mysql_cur.execute(query)
    mysql_users = mysql_cur.fetchall()

    return mysql_users


def get_contacts(mysql_cnx, user):

"""

Pega 'email', 'vcard', 'words' e 'del' da tabela contacts.

"""

    mysql_cur = mysql_cnx.cursor()

    query = ("SELECT email, vcard, words, del FROM contacts WHERE user_id = %s")
    data = (user.id, )

    mysql_cur.execute(query, data)
    mysql_contacts = mysql_cur.fetchall()

    return mysql_contacts


def save_vcard(out, vcard):

"""

Salva conteúdo `vcard` no arquivo `out` de saída.

"""

    if os.path.exists(out):
        print ("Salvando no arquivo %s" % out)
    else:
        print ("Criando aquivo: %s" % out)

    with codecs.open(out, "a", "utf-8") as fobj:
        fobj.write(vcard)
        fobj.write("\n")


def main():
    args = parse_args()
    config = load_config(args.config)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    mysql_cnx = mysql.connector.connect(buffered=True, **config["mysql"])

    users = get_users(mysql_cnx)
    for user in users:
        user = User(user[0], user[1])
        contacts = get_contacts(mysql_cnx, user)
        for contact in contacts:
            contact = Contact(contact[0], contact[1], contact[2], contact[3])
            filename = "%s_%s%s.vcf" % (user.email, user.id, "_deleted" if contact.deleted else "")
            out = os.path.join(args.out, filename)
            save_vcard(out, contact.vcard)

    mysql_cnx.close()


if __name__ == "__main__":
    main()
