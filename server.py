import http.server
import socketserver
import typing

import bs4
import requests

DOMAIN_DENY_LIST: typing.List[str] = ['i.imgur.com', 'i.minus.com', 'thecodinglove.com']
THE_CODING_LOVE_RANDOM_URL: str = 'https://thecodinglove.com/random'
PORT = 8087


def get_template(heading, content) -> str:
    return f'''
        <!DOCTYPE html>
        <html lang="">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>The Coding Love Random Simplified</title>
            <style>
                body {{
                    font-family: sans-serif;
                }}
                video {{
                    width: 100%;
                    max-width: 50em;
                    height: auto;
                }}
            </style>
        </head>
        <body>
        {heading}
        {content}
        </body>
        </html>
    '''


def is_denied_domain(data_src: str) -> bool:
    is_denied: bool = any(denied_domain for denied_domain in DOMAIN_DENY_LIST if denied_domain in data_src)
    if is_denied:
        print(data_src, 'is denied domain')
    return is_denied


def has_denied_data_content(content) -> bool:
    img = content.find('img')
    if img and img.has_attr('data-src'):
        return is_denied_domain(img['data-src'])
    return False


def get_simplified_html() -> typing.Optional[str]:
    response = requests.get(THE_CODING_LOVE_RANDOM_URL)
    soup = bs4.BeautifulSoup(response.content, features='html.parser')
    article = soup.find('article')
    content = article.find('div', class_='blog-post-content')

    if has_denied_data_content(content):
        return None
    
    heading = article.find('h1')
    return get_template(heading, content)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    @staticmethod
    def get_page() -> str:
        page = get_simplified_html()

        reload_count = 0
        while not page and reload_count < 10:
            page = get_simplified_html()
            reload_count += 1
        return page

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(self.get_page(), 'utf8'))


server = socketserver.TCPServer(('', PORT), MyHttpRequestHandler)
print(f'content url is: {THE_CODING_LOVE_RANDOM_URL}')
print(f'denied domains are: {DOMAIN_DENY_LIST}')
print(f'serving at http://localhost:{PORT}')
server.serve_forever()


