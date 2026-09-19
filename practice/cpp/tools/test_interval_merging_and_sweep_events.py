#!/usr/bin/env python3
"""Validate recorded interval solutions against straightforward references."""
import os,re,shlex,subprocess,tempfile
from pathlib import Path
COLLECTION=Path(__file__).resolve().parents[1]/"collections/b_level/interval_merging_and_sweep_events"
HARNESS=r"""
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>
long long checks=0;template<class A,class B>void same(const A&a,const B&b,const char*m){++checks;if(a!=b){std::cerr<<m<<'\n';std::exit(1);}}
template<class I>std::vector<I> merge_ref(std::vector<I> values){std::sort(values.begin(),values.end(),[](auto a,auto b){return a.start<b.start||(a.start==b.start&&a.end<b.end);});std::vector<I>out;for(auto x:values){if(out.empty()||x.start>out.back().end)out.push_back(x);else out.back().end=std::max(out.back().end,x.end);}return out;}
int main(){std::mt19937 random(20260919);for(int trial=0;trial<30000;++trial){using M=merge_sorted_closed_intervals::Interval;std::vector<M>raw;for(std::size_t i=0,n=random()%12;i<n;++i){int a=static_cast<int>(random()%21)-10,b=static_cast<int>(random()%21)-10;if(a>b)std::swap(a,b);raw.push_back({a,b});}std::sort(raw.begin(),raw.end(),[](auto a,auto b){return a.start<b.start;});same(merge_sorted_closed_intervals::merge_sorted_closed_intervals(raw),merge_ref(raw),"merge");
using N=insert_closed_interval::Interval;std::vector<N>base;for(auto x:merge_ref(raw))base.push_back({x.start,x.end});int a=static_cast<int>(random()%25)-12,b=static_cast<int>(random()%25)-12;if(a>b)std::swap(a,b);auto expected=base;expected.push_back({a,b});expected=merge_ref(expected);same(insert_closed_interval::insert_closed_interval(base,{a,b}),expected,"insert");
using X=intersect_sorted_closed_intervals::Interval;std::vector<X>left,right;for(auto x:merge_ref(raw))left.push_back({x.start,x.end});raw.clear();for(std::size_t i=0,n=random()%10;i<n;++i){int c=static_cast<int>(random()%21)-10,d=static_cast<int>(random()%21)-10;if(c>d)std::swap(c,d);raw.push_back({c,d});}for(auto x:merge_ref(raw))right.push_back({x.start,x.end});std::vector<X>intersections;for(auto l:left)for(auto rr:right){int s=std::max(l.start,rr.start),e=std::min(l.end,rr.end);if(s<=e)intersections.push_back({s,e});}std::sort(intersections.begin(),intersections.end(),[](auto p,auto q){return p.start<q.start||(p.start==q.start&&p.end<q.end);});same(intersect_sorted_closed_intervals::intersect_sorted_closed_intervals(left,right),intersections,"intersection");
using R=minimum_half_open_meeting_rooms::Interval;std::vector<R>meetings;for(std::size_t i=0,n=random()%14;i<n;++i){int start=static_cast<int>(random()%20)-10;int end=start+1+random()%8;meetings.push_back({start,end});}std::size_t rooms=0;for(auto event:meetings){std::size_t active=0;for(auto m:meetings)if(m.start<=event.start&&event.start<m.end)++active;rooms=std::max(rooms,active);}same(minimum_half_open_meeting_rooms::minimum_half_open_meeting_rooms(meetings),rooms,"rooms");}std::cout<<"Interval runtime checks passed: "<<checks<<'\n';}
"""
def completed(n):
 s=(COLLECTION/f"{n}.cpp").read_text();m=(COLLECTION/f"{n}.md").read_text();x=re.findall(r"^```cpp\n(.*?)^```$",m,re.M|re.S);d,c=re.subn(r"^([ \t]*)// Finish: .*?$",lambda q:"\n".join(q[1]+z for z in x[0].rstrip().splitlines()),s,flags=re.M);assert len(x)==1 and c==1;i=re.findall(r"^#include .*?$",d,re.M);d=re.sub(r"^#include .*?\n","",d,flags=re.M);return"\n".join(i)+f"\nnamespace {n}{{\n"+d+"}\n"
def main():
 source="\n".join(completed(x)for x in(COLLECTION/"exercise_order.md").read_text().splitlines())+HARNESS
 with tempfile.TemporaryDirectory(prefix="leetkatas-interval-")as d:
  e=Path(d)/"checks";subprocess.run(shlex.split(os.environ.get("CXX","g++"))+["-std=c++20","-Wall","-Wextra","-Werror","-O2","-D_GLIBCXX_ASSERTIONS","-x","c++","-","-o",str(e)],input=source,text=True,check=True,timeout=120);subprocess.run([str(e)],check=True,timeout=120)
if __name__=="__main__":main()
