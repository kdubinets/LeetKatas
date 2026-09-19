#!/usr/bin/env python3
"""Validate recorded backtracking solutions on exhaustive small cases."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/backtracking_and_reversible_state"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
long long checks=0;template<class A,class B>void same(A a,B b,const char*m){++checks;if(a!=b){std::cerr<<m<<'\n';std::exit(1);}}
void target_ref(const std::vector<int>&c,std::size_t i,int left,std::vector<int>&p,std::vector<std::vector<int>>&out){if(left==0){out.push_back(p);return;}if(i==c.size())return;for(int used=0;used*c[i]<=left;++used){for(int n=0;n<used;++n)p.push_back(c[i]);target_ref(c,i+1,left-used*c[i],p,out);for(int n=0;n<used;++n)p.pop_back();}}
int main(){for(std::size_t n=0;n<=9;++n)for(std::size_t k=0;k<=n;++k){std::vector<std::vector<std::size_t>>expected;for(std::size_t mask=0;mask<(std::size_t{1}<<n);++mask){std::vector<std::size_t>x;for(std::size_t i=0;i<n;++i)if((mask>>i)&1U)x.push_back(i+1);if(x.size()==k)expected.push_back(x);}std::sort(expected.begin(),expected.end());same(generate_k_combinations::generate_k_combinations(n,k),expected,"combinations");}
for(int n=0;n<=8;++n){std::vector<int>values(n);std::iota(values.begin(),values.end(),0);std::vector<std::vector<int>>expected;do{expected.push_back(values);}while(std::next_permutation(values.begin(),values.end()));std::iota(values.begin(),values.end(),0);same(permute_distinct_values::permute_distinct_values(values),expected,"permutations");}
for(unsigned mask=0;mask<64;++mask){std::vector<int>c;for(int v=1;v<=6;++v)if((mask>>(v-1))&1U)c.push_back(v);for(int target=1;target<=16;++target){std::vector<int>path;std::vector<std::vector<int>>expected;target_ref(c,0,target,path,expected);std::sort(expected.begin(),expected.end());auto got=target_sum_combinations::target_sum_combinations(c,target);std::sort(got.begin(),got.end());same(got,expected,"target combinations");}}
for(std::size_t n=0;n<=10;++n){std::vector<int>values;for(std::size_t i=0;i<n;++i)values.push_back(static_cast<int>(i/2));std::vector<std::vector<int>>expected;for(std::size_t mask=0;mask<(std::size_t{1}<<n);++mask){std::vector<int>x;for(std::size_t i=0;i<n;++i)if((mask>>i)&1U)x.push_back(values[i]);expected.push_back(x);}std::sort(expected.begin(),expected.end());expected.erase(std::unique(expected.begin(),expected.end()),expected.end());auto got=unique_subsets_from_duplicates::unique_subsets_from_duplicates(values);auto sorted=got;std::sort(sorted.begin(),sorted.end());same(sorted,expected,"unique subsets");same(got.size(),expected.size(),"subset duplicates");}
{std::vector<std::size_t>path={1};const auto saved=path;std::vector<std::vector<std::size_t>>result={{99}};generate_k_combinations::collect_k_combinations(5,3,3,path,result);same(path,saved,"restore combination path");}
{const std::vector<int>values={10,20,30};std::vector<bool>used={true,false,false};const auto saved_used=used;std::vector<int>path={10};const auto saved_path=path;std::vector<std::vector<int>>result;permute_distinct_values::collect_distinct_permutations(values,used,path,result);same(used,saved_used,"restore permutation markers");same(path,saved_path,"restore permutation path");}
{const std::vector<int>candidates={2,3,5};std::vector<int>path={2};const auto saved=path;std::vector<std::vector<int>>result;target_sum_combinations::collect_target_sum_combinations(candidates,0,6,path,result);same(path,saved,"restore target path");}
{const std::vector<int>values={1,2,2};std::vector<int>path={1};const auto saved=path;std::vector<std::vector<int>>result;unique_subsets_from_duplicates::collect_unique_subsets(values,1,path,result);same(path,saved,"restore subset path");}
const std::size_t queens[]={0,1,0,0,2,10,4,40,92,352,724};for(std::size_t n=1;n<=10;++n)same(count_n_queens_with_occupancy::count_n_queens(n),queens[n],"queens");
{std::vector<bool>columns(4,false),descending(7,false),ascending(7,false);columns[1]=descending[1]=ascending[3]=true;const auto saved_columns=columns,saved_descending=descending,saved_ascending=ascending;same(count_n_queens_with_occupancy::count_queen_placements(4,1,columns,descending,ascending),std::size_t{1},"queens from partial state");same(columns,saved_columns,"restore queen columns");same(descending,saved_descending,"restore descending diagonals");same(ascending,saved_ascending,"restore ascending diagonals");}
std::vector<std::string>grid={"ABCE","SFCS","ADEE"};for(char&c:grid[0])c=static_cast<char>(c-'A'+'a');for(char&c:grid[1])c=static_cast<char>(c-'A'+'a');for(char&c:grid[2])c=static_cast<char>(c-'A'+'a');auto original=grid;same(word_search_with_restoration::word_exists(grid,"abcced"),true,"word found");same(grid,original,"restore success");same(word_search_with_restoration::word_exists(grid,"abcb"),false,"word absent");same(grid,original,"restore failure");same(word_search_with_restoration::word_exists(grid,""),true,"empty word");std::cout<<"Backtracking runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-backtracking-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
