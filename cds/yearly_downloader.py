# BY suncong 2019
import cdsapi # usually use account: user to use this lib 
import calendar
from multiprocessing import Pool # process pool 
import argparse

# download single file contains data in a month
def downloader(year,month):
    day_range = calendar.monthrange(year,month)
    day_use = ['{:02d}'.format(iday) for iday in range(1,day_range[1]+1)]
    print ('downloading year: '+str(year)+ ' month: '+str(month))
    output = 'ERA5_'+str(year)+'_'+str(month)+'_1x1.nc'
    # download web api 
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                'divergence', 'fraction_of_cloud_cover', 'geopotential', 
                'ozone_mass_mixing_ratio', 'potential_vorticity', 'relative_humidity',
                'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind',
                'vertical_velocity',
            ],
            'pressure_level': [
                '1', '2', '3',
                '5', '7', '10',
                '20', '30', '50',
                '70', '100', '125',
                '150', '175', '200',
                '225', '250', '300',
                '350', '400', '450',
                '500', '550', '600',
                '650', '700', '750',
                '775', '800', '825',
                '850', '875', '900',
                '925', '950', '975',
                '1000',
            ],
            'year': str(year),
            'month': str(month),
            'day': day_use,
            'time': [
                '00:00', '06:00', '12:00',
                '18:00',
            ],
            'grid': '1/1',
            'area': '90/-180/-90/180',
            'format': 'netcdf',
        },
        output)
    print ('Finish download month: ' + str(month))

# user interface
parser = argparse.ArgumentParser(description='ERA5 yearly downloader')
parser.add_argument('--year', '-y', help='year of the files should be downloaded', required=True)
parser.add_argument('--month_begin','-mb',help='begin of the month',required=True)
parser.add_argument('--month_end','-me',help='end of the month',required=True)
args = parser.parse_args()


if __name__ == '__main__':
    # set processing pool
    pool = Pool(processes=4)

    # download all year
    for month in range (int(args.month_begin),int(args.month_end)+1):
        pool.apply_async(downloader,args=(int(args.year),month))
    pool.close()
    pool.join()

    print ('All files downloaded !')
