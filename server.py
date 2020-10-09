import http.server
import socketserver

import bs4
import requests

THE_CODING_LOVE_RANDOM_URL = 'https://thecodinglove.com/random'
PORT = 8087


def get_template(heading, content):
    return f'''
        <!DOCTYPE html>
        <html lang="">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>the conding love random</title>
        </head>
        <body>
        {heading}
        {content}
        </body>
        </html>
    '''


def get_simplified_html():
    response = requests.get(THE_CODING_LOVE_RANDOM_URL)
    soup = bs4.BeautifulSoup(response.content, features='html.parser')
    article = soup.find('article')
    heading = article.find('h1')
    content = article.find('div', class_='blog-post-content')
    return get_template(heading, content)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(get_simplified_html(), 'utf8'))


server = socketserver.TCPServer(('', PORT), MyHttpRequestHandler)
print(f'content url is: {THE_CODING_LOVE_RANDOM_URL}')
print(f'serving at http://localhost:{PORT}')
server.serve_forever()


