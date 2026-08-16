The code in this repository setups a database for hash-based search. This method can be used to index databases for search engines.

The primary idea of this code repository is the idea of hash-based indexing. To do hash-based indexing first choose a hash function, $f$ which approximately uniformly maps an arbitrary set of strings to a large range of integers. Then choose a large prime, $p$ . Now, define a new function $f_{n} = f \ mod \ p + 1$. Now, $f_{n}$ has range $[1,p]$. Now, form a table, $T$ with index ranging from $[1,p]$. To index a set of strings, evaluate $f_{n}$ on each string and store the string in the table, $T$,  at the index $f_{n}$ evaluates for that string. 

At time of search, evaluate the given string with $f_{n}$. If the string is written in your table you will already have the index of the string without any further operations. 

TODO: FINISH README
