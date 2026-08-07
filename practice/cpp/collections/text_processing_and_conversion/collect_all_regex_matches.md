# Name

Collect All Regular-Expression Matches

# Description

Return every non-overlapping match of a precompiled `std::regex` in a const `std::string`, preserving encounter order. Return an empty vector when nothing matches. This exercise covers traversing repeated match results with the standard regular-expression iterator.

# Solution

```cpp
std::vector<std::string> matches;
for (std::sregex_iterator it{text.begin(), text.end(), pattern}, end;
     it != end;
     ++it) {
    matches.push_back(it->str());
}
return matches;
```
