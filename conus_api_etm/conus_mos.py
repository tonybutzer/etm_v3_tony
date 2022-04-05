import time
from etmLib.log_logger import log_init, log_d, log_p
from etmLib.s3_func import s3_list_pseudo_subdirs, s3_obj_exists
from etmLib.xr_mosaic_func import xr_build_mosaic_ds, xr_write_geotiff_from_ds

bucket = 'ws-enduser'
out_prefix_path = 'ws-enduser/conus_complete/conus_mos/'  # it gets the "year" folder from the function

def _build_full_output_path(primary_name, out_prefix_path):
    a = primary_name.split('/')
    just_tif = a[-2] + '/' + a[-1]
    local_tif = a[-1]
    local_cog = 'COG_' + local_tif

    output = out_prefix_path + just_tif
    print(f'OUTPUT=={output}')

    return output



def _do_just_one_day(self, product, target_year, day, subfolders):
        log_d(f'justoneday {target_year} {day} {subfolders[0]}')

        year = target_year
        p = product
        tifs = []
        day3d = f'{day:03d}'
        for fold in subfolders:
            tif = f'{fold}{year}/{p}_{year}{day3d}.tif'
            #print(tif)
            tifs.append(tif)

        primary_name = tifs[0]  # first tif in list
        print(primary_name)
        print(f'...{primary_name} is placed at: {out_prefix_path}')
        out_obj = _build_full_output_path(primary_name, out_prefix_path)

        if not s3_obj_exists(out_obj):
            DS = xr_build_mosaic_ds(bucket, p, tifs)
            # print(DS)
            if DS is not None:
                xr_write_geotiff_from_ds(DS, primary_name, out_prefix_path)
                print('Next one')
                print('-------------------------------------------')
            else:
                print (f'No DS was created for {primary_name}')
        else:
                print (f'{primary_name} ALREADY Mosaiced wu wei')




class Conus_mosaic:

    def __init__(self, in_prefix_path, year, out_prefix_path, products):
        log_d("hello from Conus_mosaic class")
        self.in_prefix_path = in_prefix_path
        self.products = products
        self.year = year
        self.out_prefix_path = out_prefix_path
        msg = f'Mosaicking {products} in {in_prefix_path} and put it in {out_prefix_path} for {year}'
        log_d(msg)

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
        subfolders = [ x for x in subfolders if "conus_mos" not in x ]
        target_year=self.year
        product = self.products[0]
        for day in range(1,367):
            start = time.time()
            _do_just_one_day(self, product, target_year, day, subfolders)
            end = time.time()
            print(f'$$$$ MOSAIC took {end - start} SECONDS!')

