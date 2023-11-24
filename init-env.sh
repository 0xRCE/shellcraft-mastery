#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

apt update
apt -y install libseccomp-dev python3 python3-pip gdb gdbserver

pip3 install pwntools

git clone https://github.com/pwndbg/pwndbg /tmp/pwndbg
cd /tmp/pwndbg
./setup.sh

cd -
rm -rf /tmp/pwndbg


