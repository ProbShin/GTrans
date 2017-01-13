#! /usr/bin/python3
#### File Name: GTrans.py
#### Author: Xin Cheng
#### Descriptions: 
#### Created Time: Wed 12 Oct 2016 09:38:41 PM EDT

import sys,getopt
import os


README="""
#### README ####
Welcome, this is a python program to transfer graph format between
mm    - matrix market
metis - metis
[TODO] other formats

more details please visit us at https://github.com/ProbShin/MGTrans

#### USAGE ####
There are two ways:
   %s <input_graph_name> <output_graph_name>
or %s <detailed ingraph information> <detailed outgraph info>

#### For Example ####
$python3 %s foo.mtx bar.graph
$python3 %s --input foo.mtx --intype mm --output bar.graph --outtype metis
$python3 %s -i foo.mtx -s mm -o bar.graph -t metis

#### Help ####
$python3 %s --help
$python3 %s -h
"""%(sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0] )

class G_AdjacentVertex:
    def __init__(self):
        self.n = 0  # |V|
        self.m = 0  # |E| for undirected graph (i,j),(j,i) count 1, for directed count 2
        self.L = []
        self.bDirect=False
        #TODO self.EW, self.VW

def undirect_to_direct(G):
    if G.bDirect==False:
        return G
    Ltmp=[[] for _ in range(G.n)]
    for L,i in zip(G.L, range(1,G.n+1)):
        for j in L:
            if i not in G.L[j-1]:
                Ltmp[j-1].append(i);
    G.L = [l1+l2 for l1,l2 in zip(G.L,Ltmp)]
    G.bDirect = False
    return G


def metis_write(G,gname):
    if G.bDirect == True:
        G = undirect_to_direct(G)
        print("Warning, metis graph must be undirected, thus input directed graph have been transformed to undirected")
    with open(gname,"w") as f:
        print("%%metis graph by soft %s\n%d %d"%(sys.argv[0],G.n, G.m),file=f)
        for l in G.L:
            for e in l:
                print(e,file=f, end=" ")
            print("",file=f)
    return

def metis_read(gname):
    #G = G_edgelist();
    n,m = 0,0
    NCON, MCON = 0, 0
    with open(gname,"r") as f:
        for line in f:
            if line=="" or line[0]=="%":
                continue;
            head = line.split();
            if len(head)==2:
                G.n,G.m = int(head[0]),int(head[1])
            elif len(head)==3:
                G.n,G.m = int(head[0]),int(head[1])
                if(head[2]=="0"):
                    pass
                elif(head[2]=="1"):
                    NCON,MCON = 0,1
                elif(head[2]=="10"):
                    NCON,MCON = 1,0
                elif(head[2]=="11"):
                    NCON,MCON = 1,1
                else:
                    print("metis graph %s format error"%gname)
                    sys.exit(3);
            elif(len(head)==4):
                G.n,G.m = int(head[0]),int(head[1])
                if(head[2]=="0"):
                    pass
                elif(head[2]=="1"):
                    NCON,MCON = 0,1
                elif(head[2]=="10"):
                    NCON,MCON = 1,0
                elif(head[2]=="11"):
                    NCON,MCON = 1,1
                else:
                    print("metis graph %s format error"%gname)
                    sys.exit(3);
                NCON = int(head[3])
            else:
                print("metis graph %s format error"%gname)
                sys.exit(3);
            break
        for line in f:
            if line=="" or line[0]=="%":
                continue;
            G.L.append([int(e) for e in line.split()[NCON::MCON+1]])
    return G

def mm_write(G,gname):
    with open(gname,"w") as f:
        if G.bDirect ==True:
            print("%%MatrixMarket matrix coordinate pattern general",file=f)
            print("%%graph generate by %s\n%d %d %d"%(sys.argv[0],G.n,G.n,G.m),file=f)
            for L,i in zip(G.L,range(1,G.n+1)):
                for j in L:
                    print("%d %d"%(i,j),file=f)
        else:
            print("%%MatrixMarket matrix coordinate pattern symmetric",file=f)
            print("%%graph generate by %s\n%d %d %d"%(sys.argv[0],G.n,G.n,G.m),file=f)
            for L,i in zip(G.L,range(1,G.n+1)):
                for j in L:
                    if(i>j): 
                        print("%d %d"%(i,j),file=f)
    return

def mm_read(gname):
    G=G_AdjacentVertex()
    with open(gname,'r') as f:
        head=f.readline()
        if head[:33] != "%%MatrixMarket matrix coordinate ":
            print("MatrixMarket graph %s format does not support"%gname);
            sys.exit(3)
        head = head.split() 
        for line in f:
            if line=="" or line[0]=="%":
                continue
            [row,col,ent]=[int(e) for e in line.split()]
            if row is not col:
                print("MatrixMarket graph %s format does not support"%gname);
                sys.exit(3)
            G.n = row;
            break
        G.L = [[] for i in range(row)]
        if head[4]=="general":
            for line in f:
                if line=="" or line[0]=="%":
                    continue
                [i,j] = [int(e) for e in line.split()[:2]] #omit weight
                if i==j:
                    print("MatrixMarket indices on diagnal, omitted")
                    continue
                G.L[i-1].append(j)
            for L,i in zip(G.L,range(1,G.n+1)):
                for j in L:
                    if i not in G.L[j-1]:
                        G.bDirect=True
                        break
                if G.bDirect==True:
                    break
            if G.bDirect==True:
                G.m = sum([len(l) for l in G.L])
            else:
                G.m = sum([len(l) for l in G.L])//2
        else:
            if head[4] is not "symmetric":
                print("Warning, skew-symmetric or Hermitian mtx weight omitted")
            for line in f:
                if line=="" or line[0]=="%":
                    continue
                [i,j] = [int(e) for e in line.split()[:2]] #omit weight
                if i==j:
                    print("MatrixMarket indices on diagnal, omited")
                    continue
                G.L[i-1].append(j);
                G.L[j-1].append(i);
                G.m+=1
    print(G.bDirect,end=" ")
    print(G.m,end="m ")
    print(G.L)
    mm_write(G, "debug"+gname)
    return G

def guess_type_from_name(igname,ogname):
    itype, otype = None, None
    DICS={".mtx":mm, ".graph":metis,".mat":matlab}
    ipn, iext= os.path.splitext(igname);
    opn, oext= os.path.splitext(ogname);
    if iext in DICS:
        itype = DICS[iext]
    if oext  in DICS:
        otype = DICS[oext]
    return 

def usage():
    print(README)

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hi:o:v",["help","input=","output=","intype=","outtype="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    igname,ogname,igtype,ogtype="","","",""
    
    if(opts==[]):
        if(len(args)!=2):
            print("could not handle option")
            usage()
            sys.exit(2)
        igname,ogname,igtype,ogtype = guess_from_name(args[0],args[1])
    else:
        for o,a in opts:
            if o in ["-h","--help"]:
                usage()
                sys.exit(0)
            elif o in ["-i","--input"]:
                igname = a
            elif o in ["-o","--output"]:
                ogname = a
            elif o in ["--intype"]:
                igtype = a
            elif o in ["--outtype"]:
                ogtype = a
            else:
                print("could not handle option")
                usage()
                sys.exit(2)
        if igname=="" or ogname=="" or igtype=="" or ogtype=="":
            print("could not handle option")
            usage()
            sys.exit(2)
    
    if igtype.lower() == "mm" and ogtype.lower()=="metis":
        G=mm_read(igname);
        metis_write(G,ogname);
    elif igtype.lower() == "metis" and ogtype.lower()=="mm":
        G=metis_read(igname);
        mm_write(G,ogname);
    print("Success! Have tranformed %s as %s into %s as %s"%(igname,igtype,ogname,ogtype))
    return

if __name__ == "__main__":
    main()

