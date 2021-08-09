import codecs
import chardet
import cgi
import httpx
import os
from collections import defaultdict


def charset_encoding(headers):
    content_type = headers.get("Content-Type")
    if content_type is None:
        return None

    _, params = cgi.parse_header(content_type)
    if "charset" not in params:
        return None

    encoding = params["charset"].strip("'\"").lower()
    if encoding == "gb2312":
        encoding = "gbk"
    try:
        codecs.lookup(encoding)
    except LookupError:
        return None
    return encoding


def decodes_as(content, encoding):
    try:
        content.decode(encoding, errors='strict')
    except UnicodeDecodeError:
        return False
    return True


def chardet_guess(content):
    best_guess = chardet.detect(content)['encoding']
    if best_guess is not None:
        best_guess = best_guess.lower()
    if best_guess == 'gb2312':
        return "gbk"
    return best_guess


total = 0
total_with_specified_encoding = 0
total_with_utf8 = 0
total_with_successful_chardet_guess = 0
total_with_unsuccessful_chardet_guess = 0
total_with_unknown = 0

specified_charsets = defaultdict(int)
guessed_charsets = defaultdict(int)

for idx in range(1000):
    if not os.path.exists(f"content/{idx}"):
        continue

    with open(f"content/{idx}", "rb") as content_file:
        content = content_file.read()
    with open(f"headers/{idx}", "r") as headers_file:
        headers = httpx.Headers(eval(headers_file.read()))

    total += 1
    specified_encoding = charset_encoding(headers)
    if specified_encoding:
        total_with_specified_encoding += 1
        specified_charsets[specified_encoding] += 1
    else:
        if decodes_as(content, "utf-8"):
            total_with_utf8 += 1
        else:
            guess_encoding = chardet_guess(content)
            if guess_encoding:
                if decodes_as(content, guess_encoding):
                    guessed_charsets[guess_encoding] += 1
                    total_with_successful_chardet_guess += 1
                else:
                    total_with_unsuccessful_chardet_guess += 1
            else:
                total_with_unknown += 1

print("Total: ", total)
print("Total specified:          %.1f%%" % (100.0*total_with_specified_encoding/total))
print("Total utf-8:              %.1f%%" % (100.0*total_with_utf8/total))
print("Total successful guess:   %.1f%%" % (100.0*total_with_successful_chardet_guess/total))
print("Total unsuccessful guess: %.1f%%" % (100.0*total_with_unsuccessful_chardet_guess/total))
print("Total unknown:            %.1f%%" % (100.0*total_with_unknown/total))
print()
print("Specified charsets:")
for item in sorted(specified_charsets.items(), key=lambda i: i[1], reverse=True):
    print(item[0], item[1])
print()
print("Unspecfied charsets, which successfully decode as UTF-8:")
print('utf-8', total_with_utf8)
print()
print("Guessed charsets:")
for item in sorted(guessed_charsets.items(), key=lambda i: i[1], reverse=True):
    print(item[0], item[1])
