import csv
import httpx


with open("top1000.txt") as top1000:
    for row_count, line in enumerate(top1000.readlines()):
        url = line.split()[1]
        #print(row_count, url)
        try:
            r = httpx.get(url)
        except httpx.RequestError as exc:
            print(row_count, url, exc)
        else:
            print(row_count, url, r.status_code)
            with open(f"content/{row_count}", "wb") as content_file:
                content_file.write(r.content)
            with open(f"headers/{row_count}", "w") as headers_file:
                headers_file.write(repr(r.headers.raw))
