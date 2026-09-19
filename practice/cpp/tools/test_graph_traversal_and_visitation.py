#!/usr/bin/env python3
"""Validate graph-state solutions with exhaustive small graphs and grids."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/graph_traversal_and_visitation"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <queue>
#include <vector>
long long checks=0;void require(bool x,const char*m){++checks;if(!x){std::cerr<<m<<'\n';std::exit(1);}}
std::vector<std::optional<std::size_t>> distances(const std::vector<std::vector<std::size_t>>&g,std::size_t s){std::vector<std::optional<std::size_t>>d(g.size());std::queue<std::size_t>q;d[s]=0;q.push(s);while(!q.empty()){auto v=q.front();q.pop();for(auto n:g[v])if(!d[n]){d[n]=*d[v]+1;q.push(n);}}return d;}
bool cyclic(const std::vector<std::vector<std::size_t>>&g){auto n=g.size();std::vector<std::vector<bool>>r(n,std::vector<bool>(n));for(std::size_t i=0;i<n;++i)for(auto j:g[i])r[i][j]=true;for(std::size_t k=0;k<n;++k)for(std::size_t i=0;i<n;++i)for(std::size_t j=0;j<n;++j)r[i][j]=r[i][j]||(r[i][k]&&r[k][j]);for(std::size_t i=0;i<n;++i)if(r[i][i])return true;return false;}
void directed(const std::vector<std::vector<std::size_t>>&g){if(!g.empty())for(std::size_t s=0;s<g.size();++s)require(unweighted_shortest_distances::unweighted_shortest_distances(g,s)==distances(g,s),"distance");bool cycle=cyclic(g);require(detect_directed_cycle_colors::has_directed_cycle(g)==cycle,"cycle colors");auto order=topological_order_from_indegrees::topological_order(g);require(order.has_value()!=cycle,"topological presence");if(order){std::vector<std::size_t>at(g.size());for(std::size_t i=0;i<order->size();++i)at[(*order)[i]]=i;require(order->size()==g.size(),"topological size");for(std::size_t i=0;i<g.size();++i)for(auto j:g[i])require(at[i]<at[j],"topological edge");}}
void undirected(const std::vector<std::vector<std::size_t>>&g){std::vector<bool>seen(g.size());std::size_t components=0;for(std::size_t root=0;root<g.size();++root)if(!seen[root]){++components;std::vector<std::size_t>q{root};seen[root]=true;while(!q.empty()){auto v=q.back();q.pop_back();for(auto n:g[v])if(!seen[n]){seen[n]=true;q.push_back(n);}}}require(count_undirected_components::count_undirected_components(g)==components,"components");bool possible=false;for(std::size_t mask=0;mask<(std::size_t{1}<<g.size());++mask){bool ok=true;for(std::size_t i=0;i<g.size();++i)for(auto j:g[i])if(((mask>>i)&1U)==((mask>>j)&1U))ok=false;if(ok){possible=true;break;}}require(check_bipartite_coloring::has_bipartite_coloring(g)==possible,"bipartite");}
int main(){for(std::size_t n=0;n<=4;++n){std::size_t edges=n*n,limit=std::size_t{1}<<edges;for(std::size_t mask=0;mask<limit;++mask){std::vector<std::vector<std::size_t>>g(n);for(std::size_t bit=0;bit<edges;++bit)if((mask>>bit)&1U)g[bit/n].push_back(bit%n);directed(g);}}for(std::size_t n=0;n<=6;++n){std::size_t edges=n*(n-1)/2,limit=std::size_t{1}<<edges;for(std::size_t mask=0;mask<limit;++mask){std::vector<std::vector<std::size_t>>g(n);std::size_t bit=0;for(std::size_t i=0;i<n;++i)for(std::size_t j=i+1;j<n;++j,++bit)if((mask>>bit)&1U){g[i].push_back(j);g[j].push_back(i);}undirected(g);}}
for(std::size_t rows=1;rows<=3;++rows)for(std::size_t cols=1;cols<=3;++cols)for(std::size_t mask=0;mask<(std::size_t{1}<<(rows*cols));++mask){std::vector<std::vector<int>>grid(rows,std::vector<int>(cols));for(std::size_t p=0;p<rows*cols;++p)grid[p/cols][p%cols]=(mask>>p)&1U;auto got=multi_source_grid_distances::multi_source_grid_distances(grid);for(std::size_t r=0;r<rows;++r)for(std::size_t c=0;c<cols;++c){std::optional<std::size_t>best;for(std::size_t sr=0;sr<rows;++sr)for(std::size_t sc=0;sc<cols;++sc)if(grid[sr][sc]){auto d=(r>sr?r-sr:sr-r)+(c>sc?c-sc:sc-c);best=best?std::min(*best,d):d;}require(got[r][c]==best,"multi source");}}
std::cout<<"Graph runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-graph-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
