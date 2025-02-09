#!/bin/bash

# Function to check command success
check_success() {
    if [ $? -ne 0 ]; then
        echo "Error occurred in the previous command. Exiting."
        exit 1
    fi
}

pip install sxtwl requests geopy
check_success
pip install httpx[socks]
check_success
pip install -U openai
check_success
pip install qrcode[pil]
check_success
