# use in termux 
```python

pkg update && pkg upgrade -y
termux-setup-storage
pkg install python git clang openssl libffi unzip -y
pip install --upgrade pip
pip install requests psutil pyjwt aiohttp pytz cfonts protobuf pycryptodome
pip uninstall crypto pycrypto -y
pip install pycryptodome
pip install protobuf-decoder
git clone https://github.com/Ehmunna/EH-MUNNA-Bot.git
cd EH-MUNNA-Bot
python main.py


