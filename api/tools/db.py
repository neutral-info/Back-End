import datetime
import typing

from loguru import logger

from api.config import MYSQL_DATA_DATABASE
from api.tools import clients


def query(sql: str, database: str = MYSQL_DATA_DATABASE):
    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        connect.close()
        return data
    except Exception as e:
        logger.info(e)
        connect.close()
        return ""


def get_colname(table: str, database: str):
    return query(f"SHOW COLUMNS FROM {table}", database)


def get_keywords_page_sql(
    colname: str,
    table: str,
    pageNo: str,
    pageSize: str,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    bombMin: int,
    bombMax: int,
    authors: str,
    channels: str,
    producers: str,
    orderby: str,
    ordertype: str,
) -> str:

    statrIndex = (pageNo - 1) * pageSize
    sql = """
        SELECT {0}
        FROM `{1}`
        WHERE 1=1
        """.format(
        colname, table
    )

    if keywords:
        keywords_statement = []
        for k in keywords.split(","):
            k = k.strip()
            keywords_statement.append(f" `keywords` like '%{k}%' ")

        keywords_statement = "AND ( " + "OR".join(keywords_statement) + " )"
        sql = f" {sql} {keywords_statement} "

    if positions:
        position_statement = []
        for p in positions.split(","):
            p = p.strip()
            position_statement.append(f" `position` like '%{p}%'")

        position_statement = "AND ( " + " OR ".join(position_statement) + " )"
        sql = f" {sql} {position_statement} "

    if volumeMin:
        volumeRange_statement = f"AND `volume_now` >= {volumeMin}"
        sql = f" {sql} {volumeRange_statement} "

    if volumeMax:
        volumeRange_statement = f"AND `volume_now` <= {volumeMax} "
        sql = f" {sql} {volumeRange_statement} "

    if bombMin:
        bombRange_statement = f"AND `bomb_now` >= {bombMin}"
        sql = f" {sql} {bombRange_statement} "

    if bombMax:
        bombRange_statement = f"AND `bomb_now` <= {bombMax} "
        sql = f" {sql} {bombRange_statement} "

    if authors:
        authors_statement = []
        for a in authors.split(","):
            a = a.strip()
            authors_statement.append(f" `author_desc` like '%{a}%'")

        authors_statement = "AND ( " + " OR ".join(authors_statement) + " )"
        sql = f" {sql} {authors_statement} "

    if channels:
        channels_statement = []
        for c in channels.split(","):
            c = c.strip()
            channels_statement.append(f" `channel_desc` like '%{c}%'")

        channels_statement = "AND ( " + " OR ".join(channels_statement) + " )"
        sql = f" {sql} {channels_statement} "

    if producers:
        producers_statement = []
        for p in producers.split(","):
            p = p.strip()
            producers_statement.append(f" `producer_desc` like '%{p}%'")

        producers_statement = "AND ( " + " OR ".join(producers_statement) + " )"
        sql = f" {sql} {producers_statement} "

    if colname != "COUNT(*)":
        order_limit_statement = f"""
                                ORDER BY `{orderby}` {ordertype}
                                LIMIT {statrIndex}, {pageSize}
                                """
        sql = f" {sql} {order_limit_statement} "
    return sql


def get_fetch_alllist(cursor) -> list:
    desc = cursor.description
    q = [
        dict(
            zip(
                [col[0] for col in desc],
                (r.decode() if isinstance(r, bytes) else r for r in row),
            )
        )
        for row in cursor.fetchall()
    ]
    return q
    # return [
    #     dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    # ]


def create_pages_sql(
    database: str,
    table: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    bombMin: int,
    bombMax: int,
    authors: str,
    channels: str,
    producers: str,
    datatype: str,
    orderby: str,
    ordertype: str,
) -> str:
    # TODO: maybe news_id not show
    # colname = get_colname(table, database)
    colname = "COUNT(*)" if datatype == "count" else "*"
    sql = get_keywords_page_sql(
        colname,
        table,
        pageNo,
        pageSize,
        keywords,
        positions,
        volumeMin,
        volumeMax,
        bombMin,
        bombMax,
        authors,
        channels,
        producers,
        orderby,
        ordertype,
    )
    return sql


def load_pages(
    database: str = "",
    table: str = "",
    pageNo: int = None,
    pageSize: int = None,
    keywords: str = "",
    positions: str = "",
    volumeMin: int = None,
    volumeMax: int = None,
    bombMin: int = None,
    bombMax: int = None,
    authors: str = "",
    channels: str = "",
    producers: str = "",
    datatype: str = "",
    orderby: str = "",
    ordertype: str = "",
    version: str = "",
    **kwargs,
) -> typing.List[typing.Dict[str, typing.Union[str, int, float]]]:

    sql = create_pages_sql(
        database,
        table,
        pageNo,
        pageSize,
        keywords,
        positions,
        volumeMin,
        volumeMax,
        bombMin,
        bombMax,
        authors,
        channels,
        producers,
        datatype,
        orderby,
        ordertype,
    )

    logger.info(f"sql cmd:{sql}")

    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    cursor.execute(sql)
    data = get_fetch_alllist(cursor)
    cursor.close()
    connect.close()

    return data


def load_items(
    database: str = "",
    table: str = "",
):
    sql = f"SELECT DISTINCT {table}_desc FROM {table};"
    logger.info(f"sql cmd:{sql}")

    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    cursor.execute(sql)
    data = get_fetch_alllist(cursor)
    cursor.close()
    connect.close()

    return data
