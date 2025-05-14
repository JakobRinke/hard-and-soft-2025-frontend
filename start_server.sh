git pull || true
# install dependencies
./.venv/bin/pip3 install -r requirements.txt > NUL || true 
# Start the server in the background (main.py)
#./.venv/bin/python3 app.py &
./.venv/bin/python3 app.py 
# Get the PID of the last background process
pid=$!
echo "Server started with PID: $pid"