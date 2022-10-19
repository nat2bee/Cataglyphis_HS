#!/usr/local/bin/python


"""
## 18 December 2019 ##

Take a list of genes of interest and look for all transcripts possibly matching the genes names.

Developed (in my case) to use with the result table from Annocript "...filt_ann_out.txt". 
It will filter the annotation table to keep only the transcripts annotated to the genes of interest.

Usage = Find_Genes.py <options> -i <list> -t <table> 

Where: 
list = list with all the genes name (one per line)
table = table output from Annocript "...filt_ann_out.txt" with the species Taxonomy and transcripts IDs

Options: 
-h for usage help
-S search only Swissprot annotation. Default search in both (Swissprot/ Uniref) datasets.
-U search only Uniref annotation. Default search in both (Swissprot/ Uniref) datasets.

Output: filtered table will be saved under the name <gene_filtered_table>
"""

import sys, getopt

swiss_use = True
uniref_use = True

# Check for the arguments, open the inputs and print useful help messages

try:
    opts, args = getopt.getopt(sys.argv[1:],"hSUi:t:",["list=","table="])
except getopt.GetoptError:
    print '\n', '####     Invalid use     ####', '\n'
    print 'Usage = Find_Genes.py <options> -i <list> -t <table>'
    print 'For help use Find_Genes.py -h'
    sys.exit(99)
    
for opt, arg in opts:
    if len(arg) < 2 and opt == '-h':
        print '\n', 'Take a list of genes of interest and look for all transcripts possibly matching the genes names.', '\n'
        print 'Usage = Find_Genes.py <options> -i <list> -t <table> '
        print 'Where: list = list with all the genes name (one per line)'
        print 'table = table output from Annocript "...filt_ann_out.txt" with the species Taxonomy and transcripts IDs'
        print 'Options: -h for usage help'
        print '-S search only Swissprot annotation. Default search in both (Swissprot/ Uniref) datasets.'
        print '-U search only Uniref annotation. Default search in both (Swissprot/ Uniref) datasets.'
        sys.exit()
    elif len(arg) >= 2:
    	if opt in ("-S"):
    		uniref_use = False
    	if opt in ("-U"):
    		swiss_use = False
        if opt in ("-i", "--list"):
            input_list = open(arg)
        if opt in ("-t", "--table"):
            annot_table = open(arg)
            out_name = "gene_filtered_" + arg
    elif len(arg) < 2:
        print '\n', '###    Arguments are missing   ###', '\n', '\n' 'Use -h option for help\n'
        sys.exit(1)
    else:
        assert False, "unhandled option"

## Open output file
output = open(out_name,"w")

## other variables
header = True
gene_name = ""    
s_name = ""
u_name = ""
gene_list = []
    

# Make a list with input gene names
for name in input_list:
    gene_name = name.split("\n")
    gene_name = str(gene_name[0])
    gene_name = gene_name.lower() ## all to lower case for better search
    gene_list.append(gene_name)


# Check in each row of the table if this name appears
for line in annot_table:
	if header is True: # skip table header
		output.write(line)
		header = False
		continue
	
	else:
		split_line = line.split("\t")
    	s_name = str(split_line[10])
    	s_name = s_name.lower() ## all to lower case for better search
    	u_name = str(split_line[25])
    	u_name = u_name.lower() ## all to lower case for better search
    
    	
    	for gene in gene_list:
    		if swiss_use is True and uniref_use is True: # check database to compare
    			if gene in s_name or gene in u_name:
    				output.write(line)
    				continue
    		elif swiss_use is True and uniref_use is False: # check database to compare
    			if gene in s_name:
    				output.write(line)
    				continue
    		elif uniref_use is True and swiss_use is False: # check database to compare
    			if gene in u_name:
    				output.write(line)
    				continue
    		
    		

output.close()
