#Based on list of URL's available at https://v.firebog.net/hosts/csv.txt marked with "tick"
#Author: James Romeo
#Run script as Sudo
import csv
import sqlite3
import os
import logging
from urllib import request

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s -  %(levelname)s -  %(message)s',filename='pihole_update.log')

    block_list = request.urlopen("https://v.firebog.net/hosts/csv.txt")

    SUCCESS_FLAG = True
    if block_list.getcode() != 200:
        logging.error("Error connect to URL -- exiting scirpt")
        SUCCESS_FLAG = False
        quit()

    block_list = block_list.read().decode('utf-8')
    COLUMNS = ['category','ticktype','source repo','description','source URL']
    records = csv.DictReader(block_list.splitlines(),fieldnames=COLUMNS)

    try:
        con = sqlite3.connect('/etc/pihole/gravity.db')
        cur = con.cursor()
    except:
        logging.error('Error connecting to sql lite - exiting script')
        SUCCESS_FLAG = False
        quit()



    for record in records:
        if  record['ticktype'] == 'tick':
            BLOCK_LIST_URL = record['source URL']
            INSERT_STATEMENT = "INSERT OR IGNORE INTO adlist (Address) VALUES ('{}');".format(BLOCK_LIST_URL)
            try:
                cur.execute(INSERT_STATEMENT)
                con.commit()
            except:
                logging.error('Error on insert - exiting script')
                SUCCESS_FLAG = False
                break
    con.close()

    os.system('pihole -g')

    if SUCCESS_FLAG == True:
        logging.info('Successfully Updated Block List')


if __name__ == "__main__":
    main()
