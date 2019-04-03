#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:35:23 2019

@author: jwalla12
"""

#import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from Bio import Entrez
import requests

def get_args():
    parser = argparse.ArgumentParser()    
    parser.add_argument('-i', nargs=1, required=True, dest='organism')
    parser.add_argument('-e', nargs=1, required=True, dest='email')
    parser.add_argument('-r', nargs=1, required=True, dest='replicon_output')
    parser.add_argument('-s', nargs=1, required=True, dest='summary_output')    
    return parser.parse_args()

def get_handle(email, organism):    
    Entrez.email=email
    genome_handle=Entrez.esearch(db='genome', term=organism+'[orgn]', retmax='10')
    genome_result=Entrez.read(genome_handle)
    genome_id=str((genome_result['IdList']))
    genome_handle.close()
    genome_number=filter( lambda x: x in '0123456789.', genome_id )
    genome_address_text=requests.get(("https://www.ncbi.nlm.nih.gov/genome/?term="+genome_number)).text  
    genome_address_soup=BeautifulSoup(genome_address_text, 'html.parser')
    return(genome_address_soup)
    
def get_replicon_table(genome_address_soup, replicon_output):
    replicon_table=genome_address_soup.find('table',{'class':'GenomeList2'})
    replicon_table_rows=replicon_table.find_all('tr')    
    replicon_info_data=[]
    for tr in replicon_table_rows:
        td_list = tr.find_all('td')
        th_list = tr.find_all('th')
        row_data = [td.text for td in td_list]
        if th_list: 
            header_data = [th.text for th in th_list]
            replicon_info_data.append(header_data)
        replicon_info_data.append(row_data)   

    row_0=replicon_info_data[0]
    headers=[]
    for item in row_0:
        cleaned_header=item.strip()
        headers.append(cleaned_header)   
    row_1=replicon_info_data[2]
    row_2=replicon_info_data[4]   

    genomelist2=pd.DataFrame(list(zip(headers, row_1, row_2))).transpose()
    genomelist2=genomelist2.rename(columns=genomelist2.iloc[0]).drop(genomelist2.index[0])
    genomelist2.to_csv(replicon_output, sep='\t', index=False)

def get_summary_table(genome_address_soup, summary_output):
    summary_table = genome_address_soup.find('table',{'class':'summary'})
    summary_table_rows=summary_table.find_all('tr')
    summary_table_cleaned = []
    for row in summary_table_rows:
        summary_row_table_text = row.get_text()
        summary_row_table_text = summary_row_table_text.replace(u'\xa0', ' ').encode('utf-8')
        summary_table_cleaned.append(summary_row_table_text)
    summary_table_cleaned_df=pd.DataFrame(list(zip(summary_table_cleaned)))
    summary_table_cleaned_df.to_csv(summary_output, sep='\t', index=False)
    
if __name__ == '__main__':
    args = get_args()
    genome_address_soup = get_handle(args.email[0], args.organism[0])
    get_replicon_table(genome_address_soup, args.replicon_output[0])
    get_summary_table(genome_address_soup, args.summary_output[0])
    