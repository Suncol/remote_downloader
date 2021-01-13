#! /bin/bash
# by suncong 2020
# for fast download,i use a VPS as springboard
remote_server=45.77.86.185 

scp file_downloader.py root@$remote_server:/root/.
scp download_list.txt root@$remote_server:/root/.

nojump=true
while $nojump 
do 
  ssh -tt root@$remote_server << remotessh
  cd ~
  rm -f *.nc
  python3 file_downloader.py
  if [! -f "download_list.txt"]; then
    nojump=false
  fi
  exit
remotessh
rsync -avPh root@$remote_server:/root/*nc .
done

echo "alles gut!~"




