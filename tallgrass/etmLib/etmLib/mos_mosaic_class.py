import re
import sys
from .log_logger import log_init, log_d, log_p
from .log_logger import s3_save_log_file
from .s3_func import s3_list_pseudo_subdirs
from .s3_func import return_s3_list
from .xr_mosaic_func import xr_build_mosaic_ds
from .xr_mosaic_func import xr_write_geotiff_from_ds

import boto3
from botocore.errorfactory import ClientError

def s3_exists(primary_name, out_prefix_path):
    a = primary_name.split('/')
    just_tif = a[-2] + '/' + a[-1]
    output = out_prefix_path + just_tif
    print(f'Exists? {output}')
    the_bucket = output.split('/')[0]
    the_key =  '/'.join(output.split('/')[1:])
    s3 = boto3.client('s3')
    retval=True
    try:
        print(f'Exists? {output} {the_bucket} {the_key}')
        s3.head_object(Bucket=the_bucket, Key=the_key)
    except ClientError:
        print(f'Exists? FALSE')
        retval=False

    print(f'Exists? {retval}')
    log_d(f'Exists? {retval}')
    return(retval)

def _return_list_of_years(subfolders):
    THE_YEAR_LIST = []
    for path in subfolders:
        the_year = path.split('/')[-2]
        if 'log' not in the_year:
            THE_YEAR_LIST.append(the_year)
    return THE_YEAR_LIST


class Mos_mosaic:

    def __init__(self, in_prefix_path, year, out_prefix_path, products):
        log_d("hello from Mos_mosaic class")
        #self.log = log_init('Mos_mosaic')
        #self.bucket = n_bucket
        #self.in_bucket = in_bucket
        #self.out_bucket = out_bucket
        self.in_prefix_path = in_prefix_path
        self.products = products
        self.year = year
        self.out_prefix_path = out_prefix_path
        msg = f'Mosaicking {products} in {in_prefix_path} and put it in {out_prefix_path} for {year}'
        log_d(msg)

    def _return_peers(self, tif_path, subdirs):
        log_d(f'Path: {tif_path} has following subdirs: {subdirs}')
        peers = []
        a = tif_path.split('/')
        just_tif = a[-2] + '/' + a[-1]
        for dir in subdirs:
            peer = dir + just_tif
            peers.append(peer)        
        return(peers)


    def _do_just_one_day(self, target_year, subfolders):
        a = target_year.split('_')
        log_d(f'justoneday {target_year} ')
        this_year = int(a[1])
        this_day = int(a[2])
        this_day = f'{this_day:03}'
        log_d(f'justoneday {this_year} {this_day}')
        sub_sub_sub = subfolders[0] + str(this_year) + '/'
        all_tifs = return_s3_list(self.bucket, sub_sub_sub)
        target_product = self.products[0] + '_'
        tif = sub_sub_sub + target_product 
        tif = tif + str(this_year) + this_day +'.tif'
        #tif = all_tifs[0][0]
        #tif = '_'.join(tif.split('_')[0:-1])
        #tif = tif + '_' + str(this_year) + this_day +'.tif'
        log_d(f'daily file: {tif}')
        tif_peers = self._return_peers(tif, subfolders)
        primary_name = tif_peers[0]
        product = target_product
        bucket = self.bucket
        if not s3_exists(primary_name, self.out_prefix_path):
            print('Creating Mosaic');
            log_d('Creating Mosaic');
            ds = xr_build_mosaic_ds(bucket, product, tif_peers)
            xr_write_geotiff_from_ds(ds, primary_name, self.out_prefix_path)
        else:
            print(f'{primary_name} already EXISTS!')
            log_d(f'{primary_name} already EXISTS!')


    def _do_year_range(self, target_year, subfolders):
        a = target_year.split('_')
        start_year = int(a[1])
        end_year = int(a[2])
        log_d(f'From {start_year} to {end_year}')
        for year in range(start_year, end_year+1):
            log_d(f'mosaicking year: {year}')
            target_year=str(year)
            self._do_one_year(target_year,subfolders)

    
    def _do_one_year_monthly(self, target_year, subfolders):
        target_tifs = []
        sub_sub_sub = subfolders[0] + target_year + '/'
        log_p(f'subdir is: {sub_sub_sub}')
        all_tifs = return_s3_list(self.bucket, sub_sub_sub)

        target_product = self.products[0] + '_'
        # Just match the monthly sums -tony
        expression = '.*' + str(target_year) + '[0-9][0-9].tif$'

        for (tif,sz) in all_tifs:
            if target_product in tif:
                match = re.match(expression, tif)
                if match:
                    target_tifs.append(tif)

        for tif in target_tifs:
            log_d(f'monthly file: {tif}')
            tif_peers = self._return_peers(tif, subfolders)
            product = target_product
            bucket = self.bucket
            primary_name = tif_peers[0]
            if not s3_exists(primary_name, self.out_prefix_path):
                print('Creating Mosaic');
                log_d('Creating Mosaic');
                ds = xr_build_mosaic_ds(bucket, product, tif_peers)
                xr_write_geotiff_from_ds(ds, primary_name, self.out_prefix_path)
            else:
                print(f'{primary_name} already EXISTS!')
                log_d(f'{primary_name} already EXISTS!')

    def _do_one_year(self, target_year, subfolders):
        target_tifs = []
        sub_sub_sub = subfolders[0] + target_year + '/'
        log_p(f'subdir is: {sub_sub_sub}')
        all_tifs = return_s3_list(self.bucket, sub_sub_sub)

        target_product = self.products[0] + '_'
        for (tif,sz) in all_tifs:
            if target_product in tif:
                target_tifs.append(tif)

        for tif in target_tifs:
            tif_peers = self._return_peers(tif, subfolders)
            product = target_product
            bucket = self.bucket
            primary_name = tif_peers[0]
            if not s3_exists(primary_name, self.out_prefix_path):
                print('Creating Mosaic');
                log_d('Creating Mosaic');
                ds = xr_build_mosaic_ds(bucket, product, tif_peers)
                xr_write_geotiff_from_ds(ds, primary_name, self.out_prefix_path)
                log_d(f'wrote: {primary_name} {self.out_prefix_path}')
            else:
                print(f'{primary_name} already EXISTS!')
                log_d(f'{primary_name} already EXISTS!')
            
    def run_mosaic(self):
        log_d('run_mosaic')
        for prod in self.products:
            log_d(f'Mosaic this product: {prod}')

        if not self.in_prefix_path.endswith('/'):
            in_prefix_with_slash = self.in_prefix_path + '/'
        else:
            in_prefix_with_slash = self.in_prefix_path
        log_d(in_prefix_with_slash)
        subfolders,bucket = s3_list_pseudo_subdirs(in_prefix_with_slash)
        for folder in subfolders:
            print(folder)
        sub_sub = subfolders[0]
        sub_sub = bucket+'/'+sub_sub
        self.bucket=bucket
        years_list,bucket2 = s3_list_pseudo_subdirs(sub_sub)
        for year in years_list:
            log_d(year)

        target_year = self.year
        log_d(f'target year is {target_year}')
        if 'years_' in target_year:
            log_d(f'DOING ALL YEARS: {target_year}')
            self._do_year_range(target_year,subfolders)
        else:
            if 'monthly' in target_year:
                if '_' in target_year:
                    year = target_year.split('_')[-1]
                    log_d(f'DOING YEAR {year}')
                    self._do_one_year_monthly(year,subfolders)
                else:
                    log_d('DOING ALL THE YEARS')
                    years = _return_list_of_years(years_list)
                    for year in years:
                        log_d(year)
                        target_year=year
                        self._do_one_year_monthly(target_year,subfolders)
            else:
                if 'all' in target_year:
                    log_d('DOING ALL THE YEARS')
                    years = _return_list_of_years(years_list)
                    for year in years:
                        log_d(year)
                        target_year=year
                        self._do_one_year(target_year,subfolders)
                else:
                    if 'day_' in target_year:
                        log_d("do just one day")
                        self._do_just_one_day(target_year, subfolders)
                    else:
                        self._do_one_year(target_year,subfolders)


        
