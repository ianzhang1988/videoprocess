
# Xvfb -nolisten inet6 :5 -screen 0 1920x1080x24 &

# open Xvfb for opengl software render
tmp=`ps -ef | grep Xvfb | grep -v grep`
if [ -z "$tmp" ]; then
    Xvfb -nolisten inet6 :5 -screen 0 1920x1080x24 &
fi

sleep 0.5

tmp=`ps -ef | grep Xvfb | grep -v grep`
if [ -z "$tmp" ]; then
    echo "cont open Xvfb"
    exit 1
fi

export DISPLAY=:5

# start python
python3 server.py
