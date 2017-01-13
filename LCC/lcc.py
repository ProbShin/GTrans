#! /usr/bin/env python3

import sys




def DFS(nodes, n, L, i, BAN):
    if n in BAN:
        return;
    BAN.append(n);
    L[i].append(n);
    for nb in nodes[n]:
        DFS(nodes, nb, L, i, BAN);
    return


def bfs(curr_node,nodes,flg_nodes):
    for node in nodes[curr_node]:
        if flg_nodes[node]==False:
            flg_nodes[node] = True
            dfs(node,nodes,flg_nodes)
def main():
    nodes = {}
    with open(sys.argv[1],'r') as f:
        lines = f.readlines()
    for line in lines:
        if len(line)>3 and  line[0]!="#":
            x = line.split()
            n1,n2 = int(x[0]),int(x[1]);
            if n1 not in nodes:
                nodes[n1]={n2}
            else:
                nodes[n1].add(n2)
            if n2 not in nodes:
                nodes[n2]={n1}
            else:
                nodes[n2].add(n1)
    L=[]
    BAN=set() #{};
    stack=[]
    for k in nodes.keys():
        if k not in BAN:
            BAN.add(k)
            stack.append(k)
            tag = len(L)
            L.append([k])
            while len(stack) != 0:
                n = stack[-1]
                stack.pop()
                for nb in nodes[n]:
                    if nb not in BAN:
                        BAN.add(nb)
                        stack.append(nb)
                        L[tag].append(nb)
    print("there are %d connected component and their size(nodes) are "%(len(L)))
    lsize=[len(l) for l in L]
    print(lsize);
    print("The largest connected component is %d"%(max(lsize)))
    
    L = L[lsize.index(max(lsize))]
    N = len(L)
    MAP={n:i for n,i in zip(L,range(1,N+1))};

    nodes={}
    for line in lines:
        if len(line)>3 and  line[0]!="#":
            x = line.split()
            n1,n2 = int(x[0]),int(x[1]);
            if n1 in L or n2 in L:
                N1,N2 = MAP[n1],MAP[n2]
                if N1 not in nodes:
                    nodes[N1]={N2}
                else:
                    nodes[N1].add(N2)
    
    print("have mapped the subgraph into a new graph")
    M = sum([len(v) for k,v in nodes.items()])

    with open(sys.argv[1]+".mtx",'w') as f:
        f.write("%%MatrixMarket matrix coordinate pattern general\n")
        f.write("%%largest connected component of %s\n"%(sys.argv[1]))
        f.write("%xc\n")
        f.write("%d %d %d\n"%(N,N,M))
        for k,v in nodes.items():
            for e in v:
                f.write("%d %d\n"%(k,e) )
    print("have writen the new graph into %s"%(sys.argv[1]+".mtx"))
    return


    #print (node)
    flg_nodes = {}
    for node in nodes:
        flg_nodes[node] = False
    for node in nodes:
        connected_component = 0
        if flg_nodes[node] == False:
            flg_nodes[node] = True
            connected_component += 1
            dfs(node,nodes,flg_nodes)

if __name__ == "__main__":
    main();

