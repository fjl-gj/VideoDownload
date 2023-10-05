from datetime import datetime

from app.common.constantx import DB_TABLE
from app.gui.downloader.setting.database_action.basics_execute import \
    init_close_sqlite


@init_close_sqlite
def insert_single_line(cur, data):
    """
    insert single line record
    :param cur: sqlite cursor
    :param data:
                type: dict
                desc: need insert single line all data
    :return:   insert id
    """
    download_status = data.get("download_status") if data.get("download_status") else 1
    is_delete = data.get("download_status") if data.get("download_status") else 1
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"""INSERT INTO {DB_TABLE}(
    title,
    uploader,
    duration,
    quality,
    file_type,
    file_size,
    download_status,
    is_delete,
    create_time,
    update_time,
    format_id,
    url_id,
    webpage_url
    ) VALUES (
    '{data.get('title')}',
    '{data.get('uploader')}',
    '{data.get('duration')}',
    '{data.get('quality')}',
    '{data.get('file_type')}',
    '{data.get('file_size')}',
    '{download_status}',
    '{is_delete}',
    '{create_time}',
    '{update_time}',
    '{data.get("format_id")}',
    '{data.get("url_id")}',
    '{data.get("webpage_url")}'
    );"""
    cur.execute(sql).fetchall()
    return cur.lastrowid
    # return sql


def insert_multi_line(data):
    pass
