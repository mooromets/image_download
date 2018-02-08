import concurrent.futures
import urllib.request
import http.client
import re
import os
import sys

## is_header_contain
#
# Ckecks if a list of headers contain the header with a specified value in it
#
# @param head_list - a list of HTTP headers
# @param header - name of a needed header
# @param value - a value in-need
#
# @return True if a value was found
def is_header_contain(head_list, header, value):
    try:
        head = [item for item in head_list if item[0] == header][0][1]
    except Exception as exc:
        raise ValueError('Header %s is absent in a headers list' % header)
    else:
        return True if value in head else False


## unique_filename
#
# Creates an unique filename from url
def unique_filename(url):
    return re.sub('[:/\n]', '', url)


## save_image
#
# Retrieve an image from web and save it
#
# @param url
# @param timeout
# 
# @return True if url pointed to an image
def save_image(url, path, timeout):
    #open connection
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        if is_header_contain(conn.info()._headers, "Content-Type", "image"):
            #open output file with the name from url
            with open(path + '/' + unique_filename(url), 'wb') as file: 
                file.write(conn.read())
                return True
        else:
            return False

def setup_dir(dirName):
   if not os.path.isdir(dirName):
       os.makedirs(dirName)
   return dirName

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Run: savepic.py <text-file>")
        exit()

    text_file = open(sys.argv[1], "rt")
    imgLinks = text_file.read().splitlines()
    
    # retrieve pictures in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(save_image, url, setup_dir('img'), 60): url for url in imgLinks} 
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                type = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r picture saved succesfully'  % (url))
                print(type)