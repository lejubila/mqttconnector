#!/bin/bash
#echo -e "$1" | $2./piGarden.sh socket_server_command
cmd="$1"
remote_ip="$2"
remote_port="$3"

exec 5<>/dev/tcp/$remote_ip/$remote_port
echo -e "$cmd" >&5
cat <&5

