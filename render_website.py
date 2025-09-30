from jinja2 import Environment, FileSystemLoader, select_autoescape

from json import loads

from livereload import Server

from os import makedirs

from more_itertools import chunked

makedirs("pages", exist_ok=True)

with open('meta_data.json', 'r', encoding='utf-8') as file:
    books_json = file.read()

books = loads(books_json)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

pages = list(chunked(books, 10))

for i, page_books in enumerate(pages, start=1):
    rendered_page = template.render(cards=page_books, page_number=i)
    with open(f"pages/index{i}.html", "w", encoding="utf-8") as f:
        f.write(rendered_page)


def on_reload():
    rendered_page = template.render(cards=books)
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)
    print('Страница обновлена!')


server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', port=8000)
