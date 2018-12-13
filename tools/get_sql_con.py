# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: get_sql_con.py
@time: 2018/12/13
"""
from Zolo import settings
import psycopg2
from sshtunnel import SSHTunnelForwarder


def execute_query(sql=None, query_fn=None, is_select=True):
    def _query(conn, _sql=sql, _query_fn=query_fn):
        __data = None
        if query_fn is not None:
            __data = query_fn(conn)
        elif sql is not None:
            try:
                if is_select:
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    __data = cursor.fetchall()
                    cursor.close()
                    conn.commit()
                else:
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    __data = cursor.rowcount
                    conn.commit()

            except ZeroDivisionError as e:
                print(e)
            finally:
                conn.close()

        return __data

    return _do_query(query_fn=lambda conn: _query(conn))


def _do_query(query_fn, is_ssh=settings.is_ssh):
    if is_ssh:
        with SSHTunnelForwarder((settings.ssh_host, settings.ssh_port),
                                ssh_password=settings.ssh_password, ssh_username=settings.ssh_username,
                                remote_bind_address=(settings.host, settings.port)) as server:

            conn = psycopg2.connect(
                host='localhost',
                port=server.local_bind_port,
                database=settings.database,
                user=settings.user,
                password=settings.password
            )
            return query_fn(conn)
    else:
        conn = psycopg2.connect(
            host=settings.host,
            port=settings.port,
            database=settings.database,
            user=settings.user,
            password=settings.password
        )
        return query_fn(conn)