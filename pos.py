'''
Created on Jan 9, 2014

Example of using Moby and WordNet to identify part of speech, focus on whether or not a description begins with a noun.

@author: mherron
To-do:
 - handle hyphenated words (usually they are adjectives)
 - handle other plural forms (currently I only tack an 's' on)
 - handle addition of 'ed' (verbs become past-tense, nouns become adjectives) 
 - modifiers that are not separated by a hyphen (e.g., preloaded)
'''
import re

#infile format:  rid|text

infilename = "[pathname_infile].csv"
outfilename = "[pathname_results].csv"

start_line=1  # set to 1 if header (first line to process)
ind_starts_with_noun=1  # Set to 1 to add a field indicating whether description starts with a noun 

print("Start")

infile = open(infilename, "r")
lines=infile.read().splitlines()
infile.close()
print('Processing ' + str(len(lines)-start_line) + ' records.')

pos_dict={}
print ("Reading Moby-Wordnet lexical database...")
with open("[path_to_moby-wordnet_part-of-speech-file]/moby-wordnet.txt", "r") as pos_file:
    for L in pos_file:
        (term,pos)=L.split('\t')
        pos=pos.strip('|')        #Remove the pipe that separates Moby from WordNet (and then below use only the first of the remaining)
        if pos.find('N') >-1 : pos='N' #If noun is one of the acceptable parts-of-speech, let's use that
        pos=pos[0]                #If multiple remain, I use only the primary usage
        pos=pos.replace('t','V')
        pos=pos.replace('i','V')  #treat verbs, transitive verbs, and intransitive verbs as the same (for simplicity)
        pos_dict[term]=pos.strip('|')
pos_file.close()

print('Loaded ' + str(len(pos_dict)) + ' entries.')


outfile = open(outfilename, "w")



for L in range(start_line,len(lines)):
    (rid,desc)=lines[L].split('|')
    outfile.write(rid + '|' + desc + "|" )
    desc=desc.lower()
    
    #Make some replacements here, as needed
    desc=desc.replace('w/',' ')
    desc=desc.replace('f/',' ')
    desc=desc.replace('dia ','')
    desc=desc.replace('non-','')
    desc=desc.replace('high-','')
    desc=desc.replace('low-','')
    desc=desc.replace('anti-','')
    desc=desc.replace('pre-','')
    desc=desc.replace('co-','')
    desc=desc.replace('semi-','')
    desc=desc.replace('single-','')
    desc=re.sub('(\.\d+ x|\.d+x|\d+ x |\d+x |\d+ x|\d+x|\.\d+ |\.\d+||\d+ |\d+)(\.\d+ |\.\d+|\d+ |\d+)(mml|mmw|mmh|mm|cml|cmw|cmh|cm|ml|mg|g|inl|inw|inh|in|qt|oz|v)','#',desc)    # replaces everything that looks like '#...uom' 'x..X..uom'
    desc=re.sub('(\d+\.\d+)|(\d+-\d+)|(\d/\d)|(\d+\S+\d/\d)|(\.\d+)|(\d+)','#',desc)   # replace standalone numbers
    
    
    words=desc.split()
    for W in words:

        if W in pos_dict:
            outfile.write(pos_dict[W].upper())
        elif W.rstrip('s') in pos_dict:
            outfile.write(pos_dict[W.rstrip('s')].upper())
        elif W in ('#','#x#'):
            outfile.write(W)
        else:
            outfile.write('_' + W + '_')
            
    if ind_starts_with_noun==1:
        starts_with_noun=0
        W=words[0]
        if W in pos_dict and pos_dict[W].upper()=='N':
            starts_with_noun=1
        elif W.rstrip('s') in pos_dict and pos_dict[W.rstrip('s')].upper()=='N':
            starts_with_noun=1
        outfile.write('|' + str(starts_with_noun))
    outfile.write('\n')
    
outfile.close()
print("Wrote " + str(L+1-start_line) + ' lines to ' + str(outfilename))

    
print("Done")