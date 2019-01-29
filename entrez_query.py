#!/usr/bin/env python

from Bio import Entrez
import time

#this script uses BioPython Entrez to query NCBI for genomic DNA, mRNA, or protein sequence IDs and then downloads them to an output file.

#tell entrez who you are
Entrez.email="joselynn_wallace@brown.edu"

#search for a list of genomic DNA in the PRJNA13728 BioProject, read the IDs to a list called genomic_id_list, set the retmax (# of entries to retrieve) to the maximum allowable, which is 100000.
genomic_handle=Entrez.esearch(db='nucleotide', term='PRJNA13728[BioProject] AND genomic DNA[filter]', retmax='100000')
#read the output from the above handle into 'results'
genomic_result=Entrez.read(genomic_handle)
#close the handle
genomic_handle.close()
#pull out just the IDs from the results
genomic_id_list=(genomic_result['IdList'])

#search for a list of mRNA in the PRJNA13728 BioProject, read the IDs to a list called genomic_id_list
mrna_handle=Entrez.esearch(db='nucleotide', term='PRJNA13728[BioProject] AND mRNA[filter]', retmax='100000')
mrna_result=Entrez.read(mrna_handle)
mrna_handle.close()
mrna_id_list=(mrna_result['IdList'])

#search for a list of proteins in the PRJNA13728 BioProject, read the IDs to a list called genomic_id_list
protein_handle=Entrez.esearch(db='protein', term='PRJNA13728[BioProject]', retmax='100000')
protein_result=Entrez.read(protein_handle)
protein_handle.close()
protein_id_list=(protein_result['IdList'])

#look through each of the scaffold IDs and print them to a fasta file
#open up the output file ("genomic_output.fasta") as genomic_output_fasta
with open ('/Users/jwalla12/Strongylocentrotus_purpuratus/genomic_output.fasta', 'w+') as genomic_output_fasta:
    for genomic_id in genomic_id_list:
#for every ID in the list of IDs
        record=Entrez.efetch(db='nucleotide', id=genomic_id, rettype='fasta', retmode='text')
#query the nucleotide data base and pull out the fasta sequence for each entry
        time.sleep(0.5) #sleep the script so that we don't send too many queries at a time
        genomic_output_fasta.writelines(record) #write the output
        
with open ('/Users/jwalla12/Strongylocentrotus_purpuratus/mrna_output.fasta', 'w+') as genomic_output_fasta:
    for genomic_id in genomic_id_list:
        record=Entrez.efetch(db='nucleotide', id=genomic_id, rettype='fasta', retmode='text')
        time.sleep(0.5) #sleep the script so that we don't send too many queries at a time
        genomic_output_fasta.writelines(record)

with open ('/Users/jwalla12/Strongylocentrotus_purpuratus/protein_output.fasta', 'w+') as genomic_output_fasta:
    for genomic_id in genomic_id_list:
        record=Entrez.efetch(db='nucleotide', id=genomic_id, rettype='fasta', retmode='text')
        time.sleep(0.5) #sleep the script so that we don't send too many queries at a time
        genomic_output_fasta.writelines(record)        
        
#incorporate argparse to parse the search terms as arguments, also remove the full paths to outputs

        