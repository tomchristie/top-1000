# Top 1000 URLs

I've taken a dataset of top URLs from https://gtmetrix.com/top1000.html

* Ran `download.py` to download and save the content and headers.
* Then ran `analysis.py` to determine the likely character encodings.

```text
Total pages: 855

Total pages with a specified charset:                                               73.1%
Total pages with no specified charset, which successfully decode as utf-8:          22.5%
Total pages with no specified charset, which result in a successful chardet guess:   4.4%
Total pages with no specified charset, and an unsuccessful chardet guess:            0.0%
Total pages with no specified charset, and chardet returned no guess at all:         0.0%
```

Based on the results I've seen here, I think the most sensible policy for HTTPX to use
for charcter decoding would be...

* Default to whatever charset is specified, using `errors='replace'`.
* Failing that, attempt `.decode(utf-8, errors='strict')`. (Much quicker than chardet, and handles the large majority of cases.)
* Failing that, attempt chardet.

Also, it's important that the Chinese character set GB2312 should always be coerced to the superset GBK8,
since that resolves a bunch of cases that'll otherwise fail. This is important both for cases with a specified charset, and for cases where we guess with chardet.

See https://en.wikipedia.org/wiki/GBK_(character_encoding)

```
Specified charsets:
utf-8 598
gbk 8
iso-8859-1 6
shift_jis 4
euc-jp 2
iso-8859-15 2
utf8 1
iso-8859-2 1
euc-kr 1
windows-1251 1
windows-1256 1

Unspecfied charsets, which successfully decode as UTF-8:
utf-8 192

Guessed charsets:
gbk 21
shift_jis 8
euc-kr 5
windows-1252 2
iso-8859-1 1
euc-jp 1
```
