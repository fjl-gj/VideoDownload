from gui.downloader.setting.database_action.basics_execute import basics_execute, init_close_sqlite
from gui.downloader.setting.global_var_ import globals_var


@init_close_sqlite
def select_record(cur, builder):
    """
    select single line record
    :param cur: sqlite cursor
    :param builder: select query where builder
    :return: select all record
    """
    query_all = ''
    sql = f'''SELECT * FROM {globals_var.TABLE};'''
    if builder:
        for number, query in enumerate(builder):
            if number == 0 and number == len(builder) - 1:
                if type(builder[query]) == str:
                    query_all += f" {query}='{builder[query]}' "
                    break
                else:
                    query_all += f" {query}={builder[query]} "
                    break
            if number == len(builder) - 1:
                if type(builder[query]) == str:
                    query_all += f" {query}='{builder[query]}'"
                    break
                if type(builder[query]) == int:
                    query_all += f" {query}={builder[query]}"
                    break
            if type(builder[query][0]) == str:
                query_all += f" {query}='{builder[query][0]}' {builder[query][1]} "
            if type(builder[query][0]) == int:
                query_all += f" {query}={builder[query][0]} {builder[query][1]} "

        sql = f'''SELECT * FROM {globals_var.TABLE} WHERE {query_all};'''
    result = cur.execute(sql).fetchall()
    # result = basics_execute(sql, True)

    return result

