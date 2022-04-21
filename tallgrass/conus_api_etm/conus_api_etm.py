import sys
import argparse
import os


#from etmLib.mos_mosaic_class import Mos_mosaic

sys.path.append('.')
from conus_mos import Conus_mosaic
from log_logger import log_init, log_d, log_p


def _mkdir(directory):
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

def get_parser():
    parser = argparse.ArgumentParser(description='Run the conus mosaic  code')
    parser.add_argument('products', metavar='products', type=str, nargs='*',
            help='the products (netet, etasw ...)  to process - example: etasw netet')
    parser.add_argument('-y', '--year', help='specify year or Annual or all example: -y 1999 ', default='Annual', type=str)
    parser.add_argument('-i', '--in', help='input prefix_path = out/DelawareRiverBasin/Run09_13_2020/'  , default='out/wip', type=str)
    parser.add_argument('-o', '--out', help='out_prefix_path = enduser/DelawareRiverBasin/Run09_13_2020/ward_sandford_customer/' , default='enduser/wip', type=str)
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    products = args['products']
    print(products)

    if args['in']:
        print("in", args['in'])
    if args['out']:
        print("out", args['out'])


    # RUN the class Veget
    #myveg = VegET(config_directory, tile, shp, optimize)
    #myveg.run_veg_et()

    log_d('this is how you call one of your functions')

    #bucket = 'dev-et-data'
    #in_bucket = 'ws-out'
    #out_bucket = 'ws-enduser'
    in_prefix_path = args['in']
    year = args['year']
    out_prefix_path = args['out']

    mos = Conus_mosaic(in_prefix_path, year, out_prefix_path, products)
    mos.run_mosaic()
    return True


if __name__ == '__main__':
    _mkdir('log')
    log = log_init('ET_MOSAIC', 'DEBUG')

    command_line_runner()

    '''
    try:
        command_line_runner()
    except:
        print('except')
    finally:
        print('etm final bye', flush=True)
    print('etm final bye', flush=True)
    '''
