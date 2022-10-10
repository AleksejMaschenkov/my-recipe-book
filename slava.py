# -*- coding: utf-8 -*-

import email
import imaplib
import shlex
import sqlite3
from email import policy
from email.message import EmailMessage
from email.utils import parseaddr
from typing import Union


# ========================================================
#                   SQL sqlite3
# ========================================================


class SQL(object):
    def __init__(self):
        self.conn = self.create()

    def create(self):
        conn = sqlite3.connect("my_datapost.db")  # &cache=shared
        query = """CREATE TABLE IF NOT EXISTS mail_src (
                        id   INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                        uid  TEXT  UNIQUE ON CONFLICT FAIL,
                        writer STRING,
                        reader STRING,
                        src  TEXT );
                """
        conn.cursor().execute(query)
        return conn

    def insert(self, uid: str, writer: str, reader: str, src: str):
        sql = f"""INSERT INTO mail_src (uid, writer,reader, src) VALUES (?,?,?,?);"""
        try:  # for Ошибка ограничения UNIQUE
            cur = self.conn.cursor()
            cur.execute(sql, (uid, writer,reader, src))
            self.conn.commit()
            # print('Insert lastrowid=', cur.lastrowid)
        except Exception as er:
            ...
            # print(er)

    def select_uid(self, uid: str) -> Union[tuple, None]:
        if uid is None:
            raise UserWarning(f"sql parser_id -> key is None '{uid}'")

        query = f"""SELECT id, uid, writer, src FROM mail_src WHERE uid = '{uid}';"""

        cursor = self.conn.cursor()
        cursor.execute(query)
        values = cursor.fetchone()
        if values is not None:
            # REF exampl (1, '<dXalIWAre9P@devinosender.com>', ...,) or None
            return values

    def close(self):
        self.conn.close()


# ============================================================
#
# ============================================================
import base64


# https://askdev.ru/q/kodirovka-puti-k-papke-imap-imap-utf-7-dlya-python-591405/
def b64padanddecode(b):
    """Decode unpadded base64 data"""
    b += (-len(b) % 4) * '='  # base64 padding (if adds '===', no valid padding anyway)
    return base64.b64decode(b, altchars='+,', validate=True).decode('utf-16-be')


def imaputf7decode(s: str):
    """Decode a string encoded according to RFC2060 aka IMAP UTF7.

      Minimal validation of input, only works with trusted data"""
    lst = s.split('&')
    out = lst[0]
    for e in lst[1:]:
        u, a = e.split('-')  # u: utf16 between & and 1st -, a: ASCII chars folowing it
        if u == '':
            out += '&'
        else:
            out += b64padanddecode(u)
        out += a
    return out


# ============================================================
#
# ============================================================

class MailBox(object):
    imap_host = ''
    login = ''
    password = ''

    def __init__(self, imap_host, login, password):
        self.imap_host = imap_host
        self.login = login
        self.password = password
        self.mb = self.connect()

    @property
    def ok(self):
        return self.mb is not None

    def connect(self):
        mail = imaplib.IMAP4_SSL(self.imap_host, port=993)
        try:
            rv, mesasge = mail.login(self.login, self.password)
            if rv == 'OK':
                return mail
        except Exception as e:
            print(f'Error connect :{e}')

    def disconnect(self):
        if self.ok:
            # https://techoverflow.net/2019/04/08/how-to-fix-python-imap-command-close-illegal-in-state-auth-only-allowed-in-states-selected/
            self.mb.select("INBOX")
            self.mb.close()
            self.mb.logout()
            self.mb = None

    def choose(self, numb):
        if isinstance(numb, int):
            if numb < 1:
                return
            numb = str(numb)

        result, mails = self.mb.fetch(numb, '(RFC822)')
        if result == 'OK':
            return mails[0][1]

    def select_box(self, key: str = ''):
        if self.ok:
            if key is None or not key:
                rv, message_numbers = self.mb.select()
            else:
                temp = self.get_folders().get(key)
                if temp is None:
                    return
                box = temp[0]  # update
                rv, message_numbers = self.mb.select(box)  # , readonly=True)

            if rv == 'OK':
                return int(message_numbers[0])

    def get_folders(self):
        """
        Согласно RFC 3501, ответ на ответ IMAP LIST содержит следующие поля:
        Атрибуты имени, Разделитель иерархии, Имя почтового ящика
        """
        d = {}
        if self.ok:
            flag, boxs = self.mb.list()
            if flag == 'OK':
                for folder in boxs:
                    # foldef <class 'bytes'>
                    temp = shlex.split(folder.decode())
                    src: str = temp[-1]
                    d[imaputf7decode(src)] = [src, temp]
        return d

    def last(self, top=4, box='INBOX') -> [list, None]:
        if self.ok:
            count = self.select_box(box)
            print(f'COUNT in box {box} :', count)
            if count is not None:
                return [self.choose(i) for i in range(count, count - top, -1)]
        return


# ============================================================
#
# ============================================================

class MicroMail(object):

    def __init__(self, data):
        if isinstance(data, bytes):
            self.email_message = email.message_from_bytes(data,
                                                          _class=EmailMessage,
                                                          policy=policy.default)

    @property
    def uid(self):
        return self.email_message.get_all('Message-ID')[0]

    @property
    def writer(self):
        return parseaddr(self.email_message.get('From'))[1]

    @property
    def reader(self):
        try:
            addr = self.email_message.get_all('To')[0]
            return parseaddr(addr)[1]
        except:
            return '?'

# ============================================================
#
# ============================================================

def run(imap_host, mylogin, password, name_box='INBOX', count=10):
    baza = SQL()
    # -----------------------------------------
    mail_box = MailBox(imap_host, mylogin, password)
    if mail_box.ok:
        print(mail_box.get_folders())
        values = mail_box.last(count, name_box)
        if values is None:
            raise Exception('bad none')

        for src in values:
            current = MicroMail(src)
            uid = current.uid
            values = baza.select_uid(uid)
            if values is None:
                baza.insert(uid, current.writer, current.reader, src)
    # -------------------------------------------
    baza.close()


# ============================================================
#
# ============================================================

if __name__ == '__main__':
    imap_host = "imap.yandex.ru"
    mylogin = 
    password = 
    print('ЗАПИСЬ В ФАЙЛ my_datapost.db')
    run(imap_host, mylogin, password, 'INBOX', 100)
