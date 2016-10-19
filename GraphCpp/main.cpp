/*************************************************************************
    File Name: main.cpp
    Author: Xin Cheng
    Descriptions: 
    Created Time: Mon 17 Oct 2016 11:41:53 PM EDT
*********************************************************************/

#include <sstream>  /*istringstream*/
#include <fstream> /*ifstream */
#include <cstdlib>  /*exit*/
#include <cstdio>   /*stderr*/
//#include <iostream>

#include <vector>
#include <map>

using namespace std;

class GraphAAY{
public:
    GraphAAY();
    ~GraphAAY();
public:
    int N,M;
    vector<int> aayNb;
    vector<int> aayVI;
    vector<double> aayEW;
};


void read_mm_into_adjacency_array(
        string gname,               //graph name
        vector<int>&aayNb,          //adjacency array : Neighbors
        vector<int>&aayVI,          //adjacency array : Vertex Idx
        vector<double>&aayEW ,      //adjacency array : Edge Weight
        int &N,                   //graph size |V|, N
        int &M,                     //graph size |E|, M
        bool bStructOnly=false      //if true, graph's weight would be neglected 
    ){

    string sPatnType, sSymmType;
    string line;
    istringstream iss;
    int row,col,entries;
    map<int, vector<int> >    nodeList;
    map<int, vector<double> > valuList;
    ifstream in(gname.c_str());
    
    if(!in){
        fprintf(stderr, "cannot open %s as matrixmarket!\n",gname.c_str());
        exit(2);
    }

    getline(in,line);
    if(line.size()<=22+11 || line.compare(0,22+11,"%%MatrixMarket matrix coordinate ")!=0 ){
        fprintf(stderr, "does not support matrixmarket head\"%s\"\n",line.c_str());
        exit(2);
    }
    iss.str(line);
    iss>>sPatnType>>sPatnType>>sPatnType>>sPatnType>>sSymmType;

    while((!in.eof()) && (line.empty()||line[0]=='%'))
        getline(in, line);
    iss.clear();
    iss.str(line);
    iss>>row>>col>>entries;
    if(row != col){
        fprintf(stderr, "cannot process matrix market row!=col\n");
        exit(2);
    }

    //according to matrixmarket there should not be any comments between "row col entries" and "data"
    if(sPatnType=="pattern")
        if(sSymmType=="general")
            for(int i=0,rowIdx,colIdx;i<entries && !in.eof(); i++){
                getline(in,line);
                iss.clear();
                iss.str(line);
                iss>>rowIdx >>colIdx;
                if(rowIdx--==colIdx--)  //1base->0base
                    continue;
                nodeList[rowIdx].push_back(colIdx); 
            }
        else
            for(int i=0,rowIdx,colIdx;i<entries && !in.eof(); i++){
                getline(in,line);
                iss.clear();
                iss.str(line);
                iss>>rowIdx>>colIdx;
                if(rowIdx--==colIdx--)  //1base->0base
                    continue;
                nodeList[rowIdx].push_back(colIdx); 
                nodeList[colIdx].push_back(rowIdx); 
            }
    else
        if(sSymmType=="general")
            for(int i=0,rowIdx,colIdx;i<entries && !in.eof(); i++){
                double val;
                getline(in,line);
                iss.clear();
                iss.str(line);
                iss>>rowIdx >>colIdx>>val;
                if(rowIdx--==colIdx--)  //1base->0base
                    continue;
                nodeList[rowIdx].push_back(colIdx); 
                valuList[rowIdx].push_back(val);
            }
        else
            for(int i=0,rowIdx,colIdx;i<entries && !in.eof(); i++){
                double val;
                getline(in,line);
                iss.clear();
                iss.str(line);
                iss>>rowIdx>>colIdx;
                if(rowIdx--==colIdx--)  //1base->0base
                    continue;
                nodeList[rowIdx].push_back(colIdx); 
                nodeList[colIdx].push_back(rowIdx); 
                valuList[rowIdx].push_back(val); 
                valuList[colIdx].push_back(val); 
            }
    //construct the adjacency graph
    aayEW.clear();
    aayNb.clear();
    aayVI.assign(1,0);
    for(int i=0;i<row;i++) {
        aayNb.insert(aayNb.end(), nodeList[i].begin(), nodeList[i].end());
        aayVI.push_back(aayNb.size());
    }
    if( bStructOnly==false && sPatnType!="pattern")
        for(int i=0;i<row;i++)
            aayEW.insert(aayEW.end(), valuList[i].begin(), valuList[i].end());
    N=row;
    M=(sSymmType=="general")?int(aayNb.size()):int(aayNb.size())/2;
    return;
}

void dump_graph_aay(vector<int>& aayNb, vector<int>& aayVI, vector<double>&aayEW, int N, int M){
    fprintf(stderr,"\n\nGraph Size N=%d (|V|), M=%d (|E|), ",N,M);
    if(aayEW.empty())
        fprintf(stderr,"Without Weight\n");
    else
        fprintf(stderr,"With Weight\n");

    fprintf(stderr,"Vertex:\n1:%d \n",int(aayVI.size()));
    fprintf(stderr,"Edges:\n");
    for(int i=1; i<aayVI.size(); i++){
        if(aayVI[i-1]==aayVI[i])
            continue;
        fprintf(stderr,"%d:[",i);
        for(int idx=aayVI[i-1];idx<aayVI[i];idx++){
            if(aayEW.empty())
                fprintf(stderr,"%d ",aayNb[idx]+1);
            else
                fprintf(stderr,"%d(%lg) ",aayNb[idx]+1,aayEW[idx]);
        }
        fprintf(stderr,"]\n");
    }
    fprintf(stderr,"\nnb:");
    for(int i=0;i<aayNb.size(); i++)
        fprintf(stderr,"%d ",aayNb[i]);
    fprintf(stderr,"\nvi:");
    for(int i=0;i<aayVI.size(); i++)
        fprintf(stderr,"%d ",aayVI[i]);
    fprintf(stderr,"\new:");
    for(int i=0;i<aayEW.size(); i++)
        fprintf(stderr,"%lg ",aayEW[i]);
    fprintf(stderr,"\n");
}


int main( int argc, const char* argv[] ) {
    string gname="test.mtx";
    int N,M;
    vector<int> aayNb, aayVI;
    vector<double> aayEW;
    read_mm_into_adjacency_array(gname, aayNb, aayVI, aayEW,N,M,false );

    

    dump_graph_aay(aayNb,aayVI,aayEW,N,M);

    return 0;
}

