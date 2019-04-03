* `genome_info_scraping` Scrapes basic genome stats from NCBI. Takes four arguments: `-i` is the organism of interest, `-e` is the email address to provide to Entrez API, `-r` is the full path to the output file for the replicon table, `-s` is the full path to the output file for the summary table.
Example:
```
python genome_info_scraping.py -i 'Strongylocentrotus purpuratus' -e 'email@gmail.com' -r '/Users/User/Repositories/genome-stats-tools/replicon_table.txt' -s '/Users/User/Repositories/genome-stats-tools/summary_table.txt'
```
* entrez_query Uses biopython to pull sequences from ncbi
