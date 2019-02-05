#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:35:23 2019

@author: jwalla12
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

genome_page='https://www.ncbi.nlm.nih.gov/genome?term=strongylocentrotus%20purpuratus'
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

df=pd.DataFrame(table_data)


table_data=[]
for tr in genome_table_rows:
    td_list = tr.find_all('td')
    th_list = tr.find_all('th')
    row_data = [td.text for td in td_list]
    if th_list: 
        table_data.append(th_list)
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

df.to_csv('/Users/jwalla12/S_purpuratus_genome_table.txt', sep='\t', index=False)
    
