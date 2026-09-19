#!/usr/bin/env python3
"""Validate heap-frontier solutions against sorting and relaxation references."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/heap_frontier_and_streaming_state"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <optional>
#include <random>
#include <vector>
long long checks=0;template<class A,class B>void same(const A&a,const B&b,const char*m){++checks;if(a!=b){std::cerr<<m<<'\n';std::exit(1);}}
int main(){std::mt19937 r(20260919);for(int trial=0;trial<25000;++trial){std::vector<std::vector<int>>sequences(r()%10);std::vector<int>all;for(auto&sequence:sequences){sequence.resize(r()%12);for(int&v:sequence)v=static_cast<int>(r()%31)-15;std::sort(sequence.begin(),sequence.end());all.insert(all.end(),sequence.begin(),sequence.end());}std::sort(all.begin(),all.end());same(merge_k_sorted_sequences::merge_k_sorted_sequences(sequences),all,"merge frontier");std::vector<int>values(r()%35);for(int&v:values)v=static_cast<int>(r()%41)-20;std::size_t k=values.empty()?0:r()%(values.size()+1);auto sorted=values;std::sort(sorted.begin(),sorted.end());sorted.resize(k);same(retain_k_smallest_values::retain_k_smallest_values(values,k),sorted,"bounded heap");std::vector<double>medians;std::vector<int>prefix;for(int v:values){prefix.push_back(v);auto copy=prefix;std::sort(copy.begin(),copy.end());if(copy.size()%2)medians.push_back(copy[copy.size()/2]);else medians.push_back((static_cast<long long>(copy[copy.size()/2-1])+copy[copy.size()/2])/2.0);}same(running_stream_medians::running_stream_medians(values),medians,"medians");
std::size_t n=1+r()%9;std::vector<std::vector<dijkstra_shortest_distances::WeightedEdge>>g(n);for(std::size_t a=0;a<n;++a)for(std::size_t b=0;b<n;++b)if(r()%5==0)g[a].push_back({b,static_cast<long long>(r()%12)});std::size_t source=r()%n;const long long inf=std::numeric_limits<long long>::max()/4;std::vector<long long>d(n,inf);d[source]=0;for(std::size_t pass=1;pass<n;++pass)for(std::size_t a=0;a<n;++a)if(d[a]!=inf)for(auto e:g[a])d[e.to]=std::min(d[e.to],d[a]+e.weight);std::vector<std::optional<long long>>expected(n);for(std::size_t i=0;i<n;++i)if(d[i]!=inf)expected[i]=d[i];same(dijkstra_shortest_distances::dijkstra_shortest_distances(g,source),expected,"dijkstra");}std::cout<<"Heap runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-heap-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
