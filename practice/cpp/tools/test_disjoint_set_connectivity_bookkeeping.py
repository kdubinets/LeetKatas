#!/usr/bin/env python3
"""Validate recorded disjoint-set solutions with deterministic generated forests."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/disjoint_set_connectivity_bookkeeping"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
long long checks=0;void require(bool x,const char*m){++checks;if(!x){std::cerr<<m<<'\n';std::exit(1);}}
std::size_t root(const std::vector<std::size_t>&p,std::size_t x){while(p[x]!=x)x=p[x];return x;}
std::size_t halve(std::vector<std::size_t>&p,std::size_t x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;}
int main(){std::mt19937 r(20260919);for(int trial=0;trial<50000;++trial){std::size_t n=1+r()%50;std::vector<std::size_t>parent(n);std::iota(parent.begin(),parent.end(),0);for(std::size_t i=1;i<n;++i)parent[i]=r()%(i+1);std::size_t node=r()%n;auto expected_parent=parent;auto expected=halve(expected_parent,node);auto changed=parent;auto got=find_root_with_path_halving::find_root_with_path_halving(changed,node);require(got==expected,"find root");require(changed==expected_parent,"exact path halving");for(std::size_t i=0;i<n;++i)require(root(changed,i)==root(parent,i),"preserve partition");
std::size_t left=0,right=n>1?n-1:0;if(left!=right){std::vector<std::size_t>p(n);std::iota(p.begin(),p.end(),0);std::vector<std::size_t>s(n,1);s[left]=1+r()%20;s[right]=1+r()%20;const auto before_p=p,before_s=s;auto old_left=s[left],old_right=s[right];auto winner=union_distinct_roots_by_size::union_distinct_roots_by_size(p,s,left,right);auto expected_winner=old_left>=old_right?left:right;auto loser=expected_winner==left?right:left;require(winner==expected_winner,"union winner");for(std::size_t i=0;i<n;++i){const auto expected_parent=i==loser?expected_winner:before_p[i];const auto expected_size=i==expected_winner?old_left+old_right:before_s[i];require(p[i]==expected_parent,"only losing parent changes");require(s[i]==expected_size,"only surviving size changes");}}
std::vector<std::pair<std::size_t,std::size_t>>edges;for(std::size_t i=0,m=r()%100;i<m;++i)edges.emplace_back(r()%n,r()%n);std::vector<std::size_t>labels(n);std::iota(labels.begin(),labels.end(),0);std::vector<std::size_t>counts;for(auto[a,b]:edges){auto from=labels[b],to=labels[a];if(from!=to)for(auto&x:labels)if(x==from)x=to;auto distinct=labels;std::sort(distinct.begin(),distinct.end());distinct.erase(std::unique(distinct.begin(),distinct.end()),distinct.end());counts.push_back(distinct.size());}require(component_counts_after_connections::component_counts_after_connections(n,edges)==counts,"component counts");}std::cout<<"Disjoint-set runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-dsu-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
