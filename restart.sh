source env/bin/activate
sudo kill -9 $(pidof python)
rm app/nohup.out
bash ./run.sh
