#!/usr/bin/env python3

import argparse
from os.path import exists
from hdwallet import HDWallet
from hdwallet.symbols import BTC
from hdwallet.utils import is_mnemonic
import time
import requests

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Parse arguments given by user executing the tool
parser = argparse.ArgumentParser(description="Bitcoin mnemonic's passphrase bruteforcer")
parser.add_argument('-p', metavar='passphrase_list', type=str, required=True, help='Passphrase list')
parser.add_argument('-s', metavar='mnemonic_seed', type=str, required=True, help='BIP39 mnemonic seed')
args = parser.parse_args()
plist = args.p
seed_m = args.s

# Check if the provided mnemonic seed is valid
LANGUAGE: str = "english"
is_valid = is_mnemonic(mnemonic=seed_m, language=LANGUAGE)
if is_valid is False:
    quit(color.RED + 'The provided mnemonic does not respect the BIP39 standard' + color.END)
else:
    print(color.GREEN + 'Mnemonic seed accepted!' + color.END)

pl_exist = exists(plist)
if not pl_exist:
    quit(color.RED + 'Provided passphrase list not found! Please specify full path to the file' + color.END)

# Check number of passphrases to check adn show it
f = open(plist, 'r')
n = len(f.readlines())  # number of passwords to check
f.seek(0)
print(color.YELLOW + f'- - - - - - - - - -\nChecking {n} passphrases...\n- - - - - - - - - -' + color.END)

i = 0

# Initialize Bitcoin mainnet HDWallet
hdwallet: HDWallet = HDWallet(symbol=BTC)
tour = 1
while tour:
    der_t = input(color.DARKCYAN + 'How many addresses do you want to check for each derivation path?\n' + color.END)
    if der_t.isnumeric():
        tour = 0
        der = int(der_t)
        if der > 15:
            print(color.RED + 'Maybe you are overloading APIs, value set to 15' + color.END)
            der = 15
    else:
        print(color.RED + 'Please provide a number, preferably minor than 15' + color.END)
while i < n:
    addr_list = []
    passphr = f.readline().strip()
#    passphr = '' # line to check derivation with empty passphrase
    i += 1
    index = 0
    while index < der:
        ind_t = index
        hdwallet.from_mnemonic(mnemonic=seed_m, passphrase=passphr, language=LANGUAGE)
        hdwallet.from_path("m/44'/0'/0'/0/" + str(ind_t))
        addr_list.append(hdwallet.p2pkh_address())
        hdwallet.from_mnemonic(mnemonic=seed_m, passphrase=passphr, language=LANGUAGE)
        hdwallet.from_path("m/49'/0'/0'/0/" + str(ind_t))
        addr_list.append(hdwallet.p2wpkh_in_p2sh_address())
        hdwallet.from_mnemonic(mnemonic=seed_m, passphrase=passphr, language=LANGUAGE)
        hdwallet.from_path("m/84'/0'/0'/0/" + str(ind_t))
        addr_list.append(hdwallet.p2wpkh_address())
        index += 1
    print(addr_list)
    tour = 0
    # Checking activity of the addresses online
    printed = 0
    while tour < len(addr_list):
        link = 'https://blockchain.info/q/addressfirstseen/' + addr_list[tour]
        time.sleep(300/1000)  # do not overload APIs
        used = requests.get(link)
        data = used.text    # gives a string
        tour += 1
        # Determinate the derivation path
        if data != '0':
            if tour % 3 == 0:
                print(color.GREEN + f'The given seed was used with the passphrase {passphr} and the BIP84 derivation path' + color.END)
                printed = 1
            elif tour % 3 == 2:
                print(color.GREEN + f'The given seed was used with the passphrase {passphr} and the BIP49 derivation path' + color.END)
                printed = 1
            elif tour % 3 == 1:
                print(color.GREEN + f'The given seed was used with the passphrase {passphr} and the BIP44 derivation path' + color.END)
                printed = 1
    if printed == 0:
        print(color.PURPLE + f'Passphrase {passphr} not used with standard BIP44, BIP49 and BIP84 derivation path' + color.END)
