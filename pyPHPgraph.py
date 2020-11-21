#!/bin/env python3

# Hugo Gonzalez
# Nov 2020
# This program creates a graph (.dot source) from your php source code.
# You need to run it in the folder of the project, and it looks for index.php
# So you can visualize or convert to image.

# This code could be used also to investigate extra php files that are not in use
# for the project, like test files or copied files.
# It assumed that all your code should be reachable by index.php, so it visit
# each file that is called, included, referenced and create a graph

# Absolute reference, NOT FOUND and NO LINKS are used when looking for missing files
# or when looking for not used files in the source code folder.

# There is an issue with the recursive folders, it's not handled correctly, 
# so, if you have multiple folders its an option to check for each folder.

# As an example to identified unused files
#     python3 'ThisFile.py' | grep -v File | cut -f1 -d' ' | sort -u > /tmp/ax1
#     ls *php | sort > /tmp/ax2 
#     diff /tmp/ax1 /tmp/ax2  | grep '>'
# this will result in files existing but never called by the php code


import re


def getPath(filenamec):
    pat = '/'.join(filenamec.split('/')[:-1])
    if len(pat) == 0:
        pat='./'
    if pat[-1] != '/':
        pat += '/'
    if pat[1] != '/':
        pat = pat[1:]   
    return pat

def processline (line):
    #print(line)
    sp = line.split('"')
    lin1 = sp[-1]
    if lin1.find("'")>1:
        sp3 = lin1.split("'")
        lin1 = sp3[-1]
        actio = sp3[-2]
    
    if lin1.find(" ") >1 :
        sp2 = lin1.split(" ")
        lin1 = sp2[-1]
        actio = sp2[-2]
    else :
        try:
            actio = sp[-2]
        except:
            print (line)
            actio = 'unknown'
    actio = actio.strip()
    if actio.find(" ") >1 :
        actio = actio.split(" ")[-1]
    return (actio.strip(), lin1.strip())

def procfile (file1,ref):

    #pat = getPath(ref)
    pat=''
    #print("#",pat+file1)
    try:
        txt = open(pat+file1,'r').read()
    except:
        #print("File not found :", pat+file1, "from ", ref)
        return -1
    finds = re.findall(".*\.php", txt)
    links = []
    pat2 = getPath(file1)
    
    for ff in finds:
        #links.append(processline(ff, pat2))
        ac, lin = processline(ff)
        if lin.find('../') == -1 and lin[0]!='/':
            lin = pat2+lin
        links.append((ac,lin))
        
    return links

def main(princfile):
    visited = []
    tovisit = []
    tovisit.append((princfile, 'ROOT'))
    while len(tovisit) > 0 :
        for va,ref in tovisit:
            if va not in visited:
                    
                if va[0] == '/' : # absolute reference
                    print("//", va, "Absolute_reference_from ", ref)
                elif va.find('../') >= 0:
                    print("//", va, "Not_checking_UP", ref)
                    
                else:
                    links = procfile(va, ref)
                    if links == -1: # that means file not found
                        #print("//",va, "File_NOT_FOUND", ref)
                        print('\t"',va, '" -> "File_NOT_FOUND"')
                    else:
                        if len(links) == 0:
                            print('\t"', va, '" -> "NO_LINKS"')
                        else:
                            for r in links:
                                ac, vi = r
                                #print ("//",va, ac, vi )
                                print ('\t"', va, '" -> "', vi, '"' )
                                if vi not in visited and (vi,va) not in tovisit:
                                   tovisit.append((vi,va))
            tovisit.remove((va,ref))
            visited.append(va)
                        

print("digraph D {")
main('./index.php')            
print("}")
            
