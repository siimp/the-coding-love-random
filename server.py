import requests
import http.server
import socketserver
from bs4 import BeautifulSoup

THE_CODING_LOVE_RANDOM_URL = 'https://thecodinglove.com/random'
PORT = 8087

def get_simplified_html():
    response = requests.get(THE_CODING_LOVE_RANDOM_URL)
    soup = BeautifulSoup(response.content, features='html.parser')
    article = soup.find('article')
    heading = article.find('h1')
    content = article.find('div', class_='blog-post-content')

    return f'''
        <!DOCTYPE html>
        <html lang="">
        <head>
            <meta charset="utf-8">
            <title>the conding love random</title>
        </head>
        <body>
        <h1>{heading}</h1>
        {content}
        </body>
        </html>
    '''

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(get_simplified_html(), 'utf8'))
        return

with socketserver.TCPServer(('', PORT), MyHttpRequestHandler) as httpd:
    print('serving at port', PORT)
    print('content url is', THE_CODING_LOVE_RANDOM_URL)
    httpd.serve_forever()


