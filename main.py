#!/usr/bin/venv python

"""Парсер биржевых котировок.

Сохраняет документ в офрмате csv или excel с биржевыми котировками введеных или по умолчанию установленных комапний.

Usage: main.py [--filename=<name> --csv --excel --ticks=<tic list> --path=<folder>]

"""


__version__ = '1.0'


import os
import sys
import yfinance as yf
from settings import LIST_TICKS
import logging
import datetime
import argparse


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass


def download_tic(ticks: list):
    """ выгружает котировки компаний с yfinance"""
    try:
        data = yf.download(ticks)['Adj Close']
        logging.info('Данные успешно загружены')
        return data

    except TypeError as ex:
        logging.error(f'Ошибка типов передоваемых аргументов: {ex}')
        sys.exit(1)

    except Exception as ex:
        logging.error(f'Ошибка загрузки котировок: {ex}')
        sys.exit(1)


def save_csv(data, file_name: str, filepath) -> None:
    """Сохраняет котировки в формате csv"""
    name = file_name + '.csv'
    data.to_csv(os.path.join(filepath, name))
    logging.info(f'Файл успешно сохранен в формате csv: {name}')


def save_excel(data, file_name: str, filepath) -> None:
    """Сохраняет котировки в формате excel"""
    name = file_name + '.xlsx'
    data.to_excel(os.path.join(filepath, name))
    logging.info(f'Файл успешно сохранен в формате excel: {name}')


def _argparser():
    """парсер аргументов"""
    parser_ = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                      formatter_class=CustomFormatter)
    parser_.add_argument('--filename',
                         default=f'new_file({datetime.datetime.now().strftime("%m.%d.%Y-%H:%M:%S")})',
                         help='Наименование нового файла')
    parser_.add_argument('--csv',
                         action='store_true',
                         default=False,
                         help='Сохранить в формате csv')
    parser_.add_argument('--excel',
                         action='store_true',
                         default=False,
                         help='Сохранить в формате excel')
    parser_.add_argument('--path',
                         default=os.path.abspath(os.curdir),
                         help='Путь до папки, куда нужно сохраниьт результат')
    parser_.add_argument('--ticks',
                         nargs='+',
                         default=LIST_TICKS,
                         help='Сформировать список тикеров (вводится через пробел)')

    return parser_


def main(namespace) -> None:
    """управляющая функция"""

    list_ticks = namespace.ticks
    filename = namespace.filename
    data = download_tic(list_ticks)
    filepath = namespace.path

    if namespace.excel:
        save_excel(data, filename, filepath)

    if (namespace.csv is False) and namespace.excel:
        pass
    else:
        save_csv(data, filename, filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = _argparser()
    namespace_ = parser.parse_args(sys.argv[1:])
    try:
        main(namespace_)
    except Exception as e:
        logging.error(f'Произошла внештатная ошибка {e}')
        sys.exit(1)
    sys.exit(0)
