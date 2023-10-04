from app.gui.downloader.setting.database_action.basics_execute import basics_execute
from app.gui.downloader.setting.global_var_ import globals_var


def update_single_line_record(builder, update_data):
    """
    update single line record
    :param builder:  type: dict      desc: update query(where) builder  {id : [1, AND]}
    :param update_data: type: dict   desc: update data
    :return: update id
    """
    query_all = ''
    update_all = ''

    for number, query in enumerate(builder):
        if number == 0 and number == len(builder) - 1:
            query_all += f'  {query}={builder[query]} ' if type(builder[query]) == int else f'  {query}="{builder[query]}" '
            break
        if number == len(builder) - 1:
            query_all += f'  {query}={builder[query]} ' if type(builder[query]) == int else f'  {query}="{builder[query]}" '
            break
        query_all += f'  {query}={builder[query][0]} {builder[query][1]} ' if type(builder[query][0]) == int else f'  {query}="{builder[query][0]}" {builder[query][1]} '

    for number, update in enumerate(update_data):
        if number == len(update_data) - 1:
            update_all += f'  {update}={update_data[update]} ' if type(update_data[update]) == int else f'  {update}="{update_data[update]}" '
            break
        update_all += f'  {update}={update_data[update]}, ' if type(update_data[update]) == int else f'  {update}="{update_data[update]}", '

    sql = f'''UPDATE {globals_var.TABLE} SET {update_all}  WHERE {query_all};'''

    basics_execute(sql, True)

    if query_all or update_all:
        return False
    return True
