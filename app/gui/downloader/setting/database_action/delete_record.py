from app.gui.downloader.setting.database_action.basics_execute import basics_execute, init_close_sqlite
from app.gui.downloader.setting.global_var_ import globals_var


@init_close_sqlite
def delete_single_line_record(cur, builder):
    """
    delete single line record   (really delete)
    :param cur: sqlite cursor
    :param builder: delete query where builder
    :return: delete id
    """
    sql = f'''DELETE FROM {globals_var.TABLE} WHERE id={builder.get('id')};'''
    result = cur.execute(sql).fetchall()
    return result


def delete_single_line_record_alter_download_status(builder):
    """
    delete single line record   (false delete)
    :param builder: delete query where builder
    :return: delete id
    """
    sql = f'''UPDATE {globals_var.TABLE} SET is_delete=0  WHERE id={builder.get('id')};'''
    basics_execute(sql, True)
    return True
