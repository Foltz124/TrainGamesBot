import urllib.request

def _format_url(url):
    return url.replace(" ", "%20")

def get_response(url): 
    result = None 
    try:
        with urllib.request.urlopen(_format_url(url)) as response:
            result = response.read()
    except Exception as e:
        print("Unable to reach url: " + url + ". ")
        print(e)
    return result 

