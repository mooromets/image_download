tesla = ['https://3c1703fe8d.site.internapcdn.net/newman/csz/news/800/2018/5a7a9fb891072.jpg',
        'http://www.abc.net.au/news/image/9404150-3x2-700x467.jpg',
        'https://www.tflcar.com/wp-content/uploads/2018/02/Tesla-Roadster-Space-3-1024x578.png']

import concurrent.futures
import urllib.request

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

#save pic
def savepic(url):
    with open(url[-10:], 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print (response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

# retrieve a picture and save it
def savepic(url, timeout):
    #open connection
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        #open output file with the name from url
        with open(url[-15:], 'wb') as file: 
            file.write(conn.read())

# retrieve pictures in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(savepic, url, 60): url for url in tesla} 
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r picture saved succesfully'  % (url))