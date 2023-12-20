from flask import Flask, render_template, request
import requests
import random
import re
from flask import send_file
app = Flask(__name__)

def findlinks(content):
    regexquery = "\w+\.onion"
    mineddata = re.findall(regexquery, content)
    mineddata = list(dict.fromkeys(mineddata))
    return mineddata[:20], mineddata


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None

    if request.method == 'POST':
        query = request.form['query']
        if " " in query:
            query = query.replace(" ", "+")

        url = "https://ahmia.fi/search/?q={}".format(query)

        ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
                   "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                   "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
        ua = random.choice(ua_list)
        headers = {'User-Agent': ua}

        request_result = requests.get(url, headers=headers)
        content = request_result.text

        if request_result.status_code == 200:
            print("Request went through. \n")
            first_20_urls, all_urls = findlinks(content)
            results = {'first_20_urls': first_20_urls, 'all_urls': all_urls}

    return render_template('index.html', results=results)




@app.route('/download', methods=['POST'])
def download():
    all_urls = request.form.get('all_urls').split('\n')
    filename = "all_sites.txt"
    with open(filename, "w") as file:
        file.write('\n'.join(all_urls))
    return send_file(filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
