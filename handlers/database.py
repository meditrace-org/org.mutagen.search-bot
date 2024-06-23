import clickhouse_connect
import os

host = os.environ["CLICKHOUSE_HOST"]
user = os.environ["CLICKHOUSE_USER"]
pasw = os.environ["CLICKHOUSE_PASSWORD"]


def init():
    client = clickhouse_connect.get_client(host=host,
                                           username=user,
                                           password=pasw)
    client.query("""
    CREATE TABLE IF NOT EXISTS vr.query_data (
        query_uuid UUID DEFAULT generateUUIDv4(),
        score UInt32,
        query String,
        uuid UUID,
        url String,
        num UInt32,
        waited_time Float32,
        datetime DateTime,
        tg_user_id Int64 
    )
    ENGINE = MergeTree()
    PRIMARY KEY query_uuid
    """)
    client.close()


def insert_result(values):
    client = clickhouse_connect.get_client(host=host,
                                           username=user,
                                           password=pasw)
    client.insert("vr.query_data", values,
                  column_names=["score", "query", "uuid", "url", "num", "waited_time", "datetime", "tg_user_id"])
    client.close()


def count_storage():
    client = clickhouse_connect.get_client(host=host,
                                           username=user,
                                           password=pasw)
    res = client.query("SELECT COUNT(*) / 10 FROM vr.query_data").result_rows
    client.close()
    return res[0]
