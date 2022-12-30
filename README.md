# seedbf
Try to bruteforce Bitcoin mnemonic's passphrase

### Prerequisites:
Clone the repository with
```
git clone https://github.com/ASeriousMister/seedbf
```
Go to the tool's folder
```
cd seedbf
```
If you want set-up a virtual environment
```
pip3 install virtualenv
```
virtualenv sbve
```
Activate the virtual environment
```
source /sbve/bin/activate
```
Install requirements with
```
pip3 -r install requirements.txt
```

### Usage:
Now simply run the tool, like suggested:
```
seedbf.py -p passphraselist.txt -s 'abandon abandon other words'
```
## Disclaimer
This tool comes with no guarantee.
It is going to use blockchain.info's APIs. Make your own privacy conerns about that.

### ToDoList
- Electrum seeds
- Other coins
- Other languages
- API key support
