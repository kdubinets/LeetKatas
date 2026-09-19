#!/usr/bin/env python3
"""Validate recorded tree-state solutions on deterministic generated trees."""
import os, re, shlex, subprocess, tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/tree_traversal_and_recursive_state"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <random>
#include <vector>
long long checks=0; template<class A,class B> void same(A a,B b,const char*m){++checks;if(a!=b){std::cerr<<m<<'\n';std::exit(1);}}
struct Shape { std::vector<int> value,left,right,parent; };
template<class Node> struct Tree { std::vector<Node> nodes; Tree(const Shape&s):nodes(s.value.size()){for(std::size_t i=0;i<nodes.size();++i){nodes[i].value=s.value[i];nodes[i].left=s.left[i]<0?nullptr:&nodes[s.left[i]];nodes[i].right=s.right[i]<0?nullptr:&nodes[s.right[i]];}} Node* root(){return nodes.empty()?nullptr:&nodes[0];}};
std::optional<std::size_t> balance(const Shape&s,int i){if(i<0)return 0;auto l=balance(s,s.left[i]),r=balance(s,s.right[i]);if(!l||!r||(*l>*r?*l-*r:*r-*l)>1)return std::nullopt;return std::max(*l,*r)+1;}
std::size_t height_diameter(const Shape&s,int i,std::size_t&best){if(i<0)return 0;auto l=height_diameter(s,s.left[i],best),r=height_diameter(s,s.right[i],best);best=std::max(best,l+r);return std::max(l,r)+1;}
bool bst(const Shape&s,int i,std::optional<int>lo={},std::optional<int>hi={}){if(i<0)return true;if((lo&&s.value[i]<=*lo)||(hi&&s.value[i]>=*hi))return false;return bst(s,s.left[i],lo,s.value[i])&&bst(s,s.right[i],s.value[i],hi);}
long long digits(const Shape&s,int i,long long prefix=0){if(i<0)return 0;auto now=prefix*10+s.value[i];if(s.left[i]<0&&s.right[i]<0)return now;return digits(s,s.left[i],now)+digits(s,s.right[i],now);}
void inorder(const Shape&s,int i,std::vector<int>&out){if(i<0)return;inorder(s,s.left[i],out);out.push_back(s.value[i]);inorder(s,s.right[i],out);}
int lca(const Shape&s,int a,int b){std::vector<bool>seen(s.value.size());for(int x=a;x>=0;x=s.parent[x])seen[x]=true;for(int x=b;x>=0;x=s.parent[x])if(seen[x])return x;return -1;}
Shape make_shape(std::mt19937&r,int n){Shape s; s.value.resize(n);s.left.assign(n,-1);s.right.assign(n,-1);s.parent.assign(n,-1);for(int&i:s.value)i=static_cast<int>(r()%21)-10;for(int child=1;child<n;++child){for(;;){int p=r()%child;if(s.left[p]<0&&s.right[p]<0){if(r()%2)s.left[p]=child;else s.right[p]=child;s.parent[child]=p;break;}if(s.left[p]<0){s.left[p]=child;s.parent[child]=p;break;}if(s.right[p]<0){s.right[p]=child;s.parent[child]=p;break;}}}return s;}
void test(const Shape&s){
 {Tree<balanced_tree_height::TreeNode>t(s);same(balanced_tree_height::balanced_tree_height(t.root()),balance(s,s.value.empty()?-1:0),"balance");}
 {Tree<tree_diameter_in_edges::TreeNode>t(s);std::size_t expected=0;height_diameter(s,s.value.empty()?-1:0,expected);same(tree_diameter_in_edges::tree_diameter_in_edges(t.root()),expected,"diameter");}
 {Tree<validate_strict_bst_bounds::TreeNode>t(s);same(validate_strict_bst_bounds::is_strict_binary_search_tree(t.root()),bst(s,s.value.empty()?-1:0),"bst");}
 Shape d=s;for(int&v:d.value)v=(v+10)%10;{Tree<sum_root_to_leaf_numbers::TreeNode>t(d);same(sum_root_to_leaf_numbers::sum_root_to_leaf_numbers(t.root()),digits(d,d.value.empty()?-1:0),"digits");}
 if(!s.value.empty()){std::vector<int>order;inorder(s,0,order);Tree<kth_inorder_value::TreeNode>t(s);for(std::size_t k=1;k<=order.size();++k)same(kth_inorder_value::kth_inorder_value(t.root(),k),order[k-1],"inorder");}
 if(s.value.size()>1){Tree<lowest_common_ancestor::TreeNode>t(s);for(std::size_t a=0;a<s.value.size();++a)for(std::size_t b=a+1;b<s.value.size();++b){auto*actual=lowest_common_ancestor::lowest_common_ancestor(t.root(),&t.nodes[a],&t.nodes[b]);same(actual,&t.nodes[lca(s,a,b)],"lca");}}
}
int main(){std::mt19937 r(20260919);for(int n=0;n<=20;++n)for(int trial=0;trial<150;++trial)test(make_shape(r,n));std::cout<<"Tree runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-tree-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
