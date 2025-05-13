gh pull
# Start the server in the background (main.py)
python3 main.py &
# Get the PID of the last background process
pid=$!
echo "Server started with PID: $pid"