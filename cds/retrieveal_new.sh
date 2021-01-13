#! /bin/bash
# by suncong 2020
# for fast download,i use a VPS as springboard
# because of the storge limit of vps, we choose download 4 month asynchronously
download_year="$1" # make sure there is no space
remote_server=149.28.67.2

ssh -tt root@$remote_server << remotessh
echo ${download_year}
python yearly_downloader.py -y ${download_year} -mb 1 -me 4 >> log
python yearly_downloader.py -y ${download_year} -mb 5 -me 8  & { sleep 10; pkill -9 -f yearly_downloader.py & }
exit
remotessh
rsync -avPh root@$remote_server:/root/ERA5* .
ssh -tt root@$remote_server << remotessh
rm -f ERA5*
exit
remotessh
echo done!

ssh -tt root@$remote_server << remotessh
python yearly_downloader.py -y ${download_year} -mb 5 -me 8 >> log
python yearly_downloader.py -y ${download_year} -mb 9 -me 12  & { sleep 10; pkill -9 -f yearly_downloader.py & }
exit
remotessh
rsync -avPh root@$remote_server:/root/ERA5* .
ssh -tt root@$remote_server << remotessh
rm -f ERA5*
exit
remotessh
echo done!

ssh -tt root@$remote_server << remotessh
python yearly_downloader.py -y ${download_year} -mb 9 -me 12 >> log
exit
remotessh
rsync -avPh root@$remote_server:/root/ERA5* .
ssh -tt root@$remote_server << remotessh
rm -f ERA5*
exit
remotessh
echo done!

