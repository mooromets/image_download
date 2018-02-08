import concurrent.futures
import urllib.request
import re
import os
import sys
import time


## save_image
#
# Retrieve an image from web and save it
#
# @param url
# @param timeout
# 
# @return True if url pointed to an image
#
def save_image(url, path, timeout):
    #open connection
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        if match_header(conn.info()._headers, "Content-Type", "image"):
            #open output file with the name from url
            with open(path + '/' + unique_filename(url), 'wb') as file: 
                file.write(conn.read())
                return True
        else:
            return False


## download_files
#
# Download a number of files in parallel
#
# @param imageLinks a list containing the links
# @param toDir output directory
# @param threads number of threads
# @param timeout timeout for each file
#
def download_files(imageLinks, toDir = 'img', threads = 4, timeout = 60):
    print('%d files are in a list'  % len(imageLinks))
    # retrieve pictures in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(save_image, url, setup_dir(toDir), timeout): url for url in imageLinks} 
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                res = future.result()
            except Exception as exc:
                print('URL: %r generated an exception: %s' % (url, exc))
            else:
                if not res:
                    print('URL: %r was not an image file'  % (url))


## match_header
#
# Ckeck if a list of headers contains the header with a specified value in it
#
# @param head_list - a list of HTTP headers
# @param header - name of a needed header
# @param value - a value in-need
#
# @return True if a value was found
#
def match_header(head_list, header, value):
    try:
        head = [item for item in head_list if item[0] == header][0][1]
    except Exception as exc:
        raise ValueError('Header %s is absent in a headers list' % header)
    else:
        return True if value in head else False


## unique_filename
#
# Create an unique filename from url
#
# @param url
#
# @return filename  
#
def unique_filename(url):
    return re.sub('[:/]', '', url)


## setup_dir
# 
# Set up an output directory
#
# @param dirName
#
def setup_dir(dirName):
   if not os.path.isdir(dirName):
       os.makedirs(dirName)
   return dirName


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Run: savepic.py <text-file>")
        exit()

    start_time = time.time()
    
    with open(sys.argv[1], "rt") as text_file: 
        download_files(text_file.read().splitlines())

    print("Processed in %f seconds" % (time.time() - start_time))