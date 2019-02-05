#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:35:23 2019

@author: jwalla12
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from Bio import Entrez

parser = argparse.ArgumentParser()

parser.add_argument('-i', nargs=1, required=True, dest='organism')
parser.add_argument('-e', nargs=1, required=True, dest='email')
parser.add_argument('-o', nargs=1, required=True, dest='output')

args=parser.parse_args()

Entrez.email=args.email[0]

genome_handle=Entrez.esearch(db='genome', term=args.organism[0]+'[orgn]', retmax='10')
genome_result=Entrez.read(genome_handle)
genome_id=(genome_result['IdList'])
genome_handle.close()

genome_id=str(genome_id)
genome_number=filter( lambda x: x in '0123456789.', genome_id )
genome_page="https://www.ncbi.nlm.nih.gov/genome/?term="+genome_number

genome_page_html=urllib2.urlopen(genome_page)
soup=BeautifulSoup(genome_page_html, 'html.parser')

genome_table=soup.find('table',{'class':'GenomeList2'})
genome_table_rows=genome_table.find_all('tr')

table_data=[]
for tr in genome_table_rows:
    td_list = tr.find_all('td')
    th_list = tr.find_all('th')
    row_data = [td.text for td in td_list]
    if th_list: 
        header_data = [th.text for th in th_list]
        table_data.append(header_data)
    table_data.append(row_data)
 
row_0=table_data[0]
headers=[]
for item in row_0:
    cleaned_header=item.strip()
    headers.append(cleaned_header)   
row_1=table_data[2]
row_2=table_data[4]   


df=pd.DataFrame(list(zip(headers, row_1, row_2))).transpose()
df=df.rename(columns=df.iloc[0]).drop(df.index[0])

df.to_csv(args.output[0], sep='\t', index=False)
    
#
#
#########
#    
#   # Strongylocentrotus purpuratus
#
#import urllib2
#from bs4 import BeautifulSoup
#import pandas as pd
#import argparse
#from Bio import Entrez
#   
#Entrez.email='joselynn_wallace@brown.edu'
#
#genome_handle=Entrez.esearch(db='genome', term='Strongylocentrotus purpuratus [orgn]', retmax='10')
#genome_result=Entrez.read(genome_handle)
#genome_id=(genome_result['IdList'])
#genome_handle.close()
#
#genome_id=str(genome_id)
#genome_number=filter( lambda x: x in '0123456789.', genome_id )
#genome_page="https://www.ncbi.nlm.nih.gov/genome/?term="+genome_number
#
#genome_page_html=urllib2.urlopen(genome_page)
#soup=BeautifulSoup(genome_page_html, 'html.parser')
#
#genome_table=soup.find('table',{'class':'GenomeList2'})
#genome_table_rows=genome_table.find_all('tr')
#
#table_data=[]
#for tr in genome_table_rows:
#    td_list = tr.find_all('td')
#    th_list = tr.find_all('th')
#    row_data = [td.text for td in td_list]
#    if th_list: 
#        header_data = [th.text for th in th_list]
#        table_data.append(header_data)
#    table_data.append(row_data)
# 
#row_0=table_data[0]
#headers=[]
#for item in row_0:
#    cleaned_header=item.strip()
#    headers.append(cleaned_header)   
#row_1=table_data[2]
#row_2=table_data[4]   
#
#
#df=pd.DataFrame(list(zip(headers, row_1, row_2))).transpose()
#df=df.rename(columns=df.iloc[0]).drop(df.index[0])
#
#df.to_csv('/Users/jwalla12/testing4.txt', sep='\t', index=False)
