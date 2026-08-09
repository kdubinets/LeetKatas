# Name

Call a Dependent Member Template

# Description

Call the zero-argument member template `read<int>()` on `source` and return its result. Since the member access depends on the `Source` template parameter, disambiguate `read` as a template before supplying its template argument.

# Solution

```cpp
return source.template read<int>();
```
