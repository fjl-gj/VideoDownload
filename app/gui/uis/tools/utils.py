from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps, partial

EXECUTOR = ThreadPoolExecutor(max_workers=8)


def max_h_w(ui_obj, h, w):
    """
    setting max widget height width
    :param ui_obj:  widget objects
    :param h:       height
    :param w:       width
    :return:        None
    """
    ui_obj.setMaximumHeight(h)
    ui_obj.setMaximumWidth(w)


def min_h_w(ui_obj, h, w):
    """
    setting mix widget height width
    :param ui_obj:  widget objects
    :param h:       height
    :param w:       width
    :return:        None
    """
    ui_obj.setMinimumHeight(h)
    ui_obj.setMinimumWidth(w)


def default_thread_index(value, threads):
    """
    find index in threads array value
    :param value:
    :param threads:
    :return:
    """
    value_index = threads.index(value)
    return value_index


def table_sort_display(values):
    data = [i for i in values if i["filesize"]]
    # audio = []
    # video = []
    # for i in data:
    #     if
    format_type = sorted(
        data,
        key=lambda fomart: (fomart["quality"], fomart["format_note"], fomart["ext"]),
        reverse=True,
    )
    return format_type


def run_in_thread_pool(*, callbacks=(), callbacks_kwargs=()):
    """将函数放入线程池执行的装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            future = EXECUTOR.submit(func, *args, **kwargs)
            for index, callback in enumerate(callbacks):
                try:
                    kwargs = callbacks_kwargs[index]
                except IndexError:
                    kwargs = None
                fn = partial(callback, **kwargs) if kwargs else callback
                future.add_done_callback(fn)
            return future

        return wrapper

    return decorator


def replace_other_char(strings):
    """
    Replaces characters other than Chinese characters and identifiers
    :param strings: need replaces string
    :return: new string
    """
    new_string = ""
    for i in strings:
        if "\u4e00" <= i <= "\u9fff":
            new_string += i
        elif i.isalnum() or i == "_":
            new_string += i
        else:
            new_string += "_"
    return new_string
