The code in this repository setups a database for hash-based search. This method can be used to index databases for search engines.

The primary idea of this code repository is the idea of hash-based indexing. To do hash-based indexing first choose a hash function, $f$ which approximately uniformly maps an arbitrary set of strings to a large range of integers. Then choose a large prime, $p$ . Now, define a new function $f_{n} = f \ mod \ p + 1$. Now, $f_{n}$ has range $[1,p]$. Now, form a table, $T$ with index ranging from $[1,p]$. To index a set of strings, evaluate $f_{n}$ on each string and store the string in the table, $T$,  at the index $f_{n}$ evaluates for that string. 

At time of search, evaluate the given string with $f_{n}$. If the string is written in your table you will already have the index of the string without any further operations.

In the case of collisions one can store an array of strings at the index the strings are written in and search through the array at time of search. There are other ways to handle collisions such as linear probing that I did not use in my codebase. 

The algorithm described above is often referred to as other names as well, some examples include: dictionary, hash-table, and hash-map. 

Hash-indexing has the advantage over binary search that hash-indexing is almost always much faster than binary search. The disadvantages of hash-indexing which I believe is usually outweighed by its advantages are larger space requirements and databases which do not store similar values close to each other. This makes it difficult to naively use hash-indexing for fuzzy search. The code in this repository fixes the issue of fuzzy search and is why I refer to it as hash-based search.

To perform hash-based search, one first needs some metric, $M$, which allows for ordering the set of searchable strings, $\Omega$, from more desirable to appear first in search results to less desirable. Then, obtain all the prefixes for your searchable strings, hash-index all of the observed prefixes and with each prefix store the $n$ most desirable full search terms associated with that prefix remaining in $\Omega$. Remove the $n$ strings from $\Omega$. Iterate this process until $\Omega$ is empty. This setups a database for hash-based search.

At time of search, hash all the prefixes of the search input and store each of the groups of the $n$ most desirable full search terms. In the case of an online search engine, one will likely want to send these strings to the client. Then, using frontend software, the client's machine will filter these results in the most desirable order dependent on their input string. The sum of the groups of $n$ should be small and even naive algorithms should be able to filter these search terms fast enough. One may want to also store the values of $M$ along with the full search terms and also use $M$ to order the results on the client side. 

