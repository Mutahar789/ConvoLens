source env/bin/activate
cd app
nohup streamlit run app.py --server.port 8000 --theme.base "dark" --server.fileWatcherType none &
