# Originally from:
# https://kamal.io/blog/exporting-email-threads-from-gmail-into-csv-file

import argparse
from datetime import datetime
import mailbox
import csv
import pathlib
import re
from email.header import decode_header

patterns = [
    re.compile(r'[\s\S]+You\smade\sa\spurchase\sat:[\s\S]*\d\d:\d\d[\s]*(.+)On\sthis\scard[\s\S]*bank\sstatement\sas:([\s\S]+)Generated\son\s([\s\S]+)==[\s]+Share'), # has share statement at the end
    re.compile(r'[\s\S]+You\smade\sa\spurchase\sat:[\s\S]*\d\d:\d\d(?:\sUTC)?([\s\S]+)On\sthis\scard[\s\S]*bank\sstatement\sas:([\s\S]+)Something[\s\S]+Generated\son\s([\s\S]+?)<'), # no share statement at the end
    re.compile(r'[\s\S]+You\smade\sa\spurchase\sat:[\s\S]*\d\d:\d\d[\s]*(.+)On\sthis\scard[\s\S]*bank\sstatement\sas:([\s\S]+)Generated\son\s([\s\S]+?)<') # has share statement at the end
]

date_format = "%d %B %Y %H:%M UTC"

def parse_body(content):
    match = None
    for pattern in patterns:
        match = pattern.match(content)
        if match != None:
            break

    if match != None:
        foreign = match.group(1).strip()
        message = match.group(2).strip()
        datetime_str = match.group(3).strip()

        dt = datetime.strptime(datetime_str, date_format)

        return (foreign, message, dt)
    else:
        return None

def write_csv(input):

    pathlib.Path("target").mkdir(exist_ok=True)
    transactions = {}

    for message in mailbox.mbox(input):
        if message.is_multipart():
            content = ''.join(part.get_payload(decode=True).decode("utf8") for part in message.get_payload() if part.get_content_type() == 'text/plain')
        else:
            content = message.get_payload(decode=True)

        parsed = parse_body(content)
        if parsed != None:
            subject = message['subject']
            decoded = decode_header(subject)[0][0]
            try:
                decoded_str = decoded.decode("utf8")
            except:
                pass # fine if it is already str
            amount = decoded_str.split(" for ")[-1].strip("€")
            (foreign, message, dt) = parsed

            key = datetime.strftime(dt, "%Y-%m")
            if transactions.get(key) == None:
                transactions[key] = []

            transactions[key].append((dt, message, amount))
        else:
            print("Unable to parse " + message["message-id"])
            with open("target/unparsed-" + message["message-id"].strip("<>") + ".txt", "w") as f:
                f.write(content)

    for key, trans in transactions.items():
        trans.sort()
        writer = csv.writer(open("target/trans-" + key + ".csv", "w"))
        for row in trans:
            writer.writerow(row)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input MBOX file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    write_csv(args.input)
