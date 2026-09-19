#!/usr/bin/env python3
"""Exhaustively validate partition and quickselect recorded solutions."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/partition_and_selection_idioms"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>
long long checks=0;void require(bool x,const char*m){++checks;if(!x){std::cerr<<m<<'\n';std::exit(1);}}
int main(){for(std::size_t n=0;n<=7;++n){std::size_t count=1;for(std::size_t i=0;i<n;++i)count*=5;for(std::size_t code=0;code<count;++code){std::size_t rest=code;std::vector<int>values(n);for(int&v:values){v=static_cast<int>(rest%5)-2;rest/=5;}auto sorted=values;std::sort(sorted.begin(),sorted.end());for(int pivot=-3;pivot<=3;++pivot){auto copy=values;auto bounds=three_way_partition_around_pivot::three_way_partition_around_pivot(copy,pivot);require(bounds.first<=bounds.second&&bounds.second<=copy.size(),"bounds");for(std::size_t i=0;i<bounds.first;++i)require(copy[i]<pivot,"less region");for(std::size_t i=bounds.first;i<bounds.second;++i)require(copy[i]==pivot,"equal region");for(std::size_t i=bounds.second;i<copy.size();++i)require(copy[i]>pivot,"greater region");auto after=copy;std::sort(after.begin(),after.end());require(after==sorted,"partition multiplicity");}for(std::size_t rank=0;rank<n;++rank){auto copy=values;require(quickselect_with_partition_helper::quickselect_with_partition_helper(copy,rank)==sorted[rank],"quickselect value");std::sort(copy.begin(),copy.end());require(copy==sorted,"quickselect multiplicity");}}}std::cout<<"Partition runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-partition-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
