from jinja2 import Environment, FileSystemLoader, select_autoescape
from json import loads
from livereload import Server
from os import makedirs
from more_itertools import chunked
from argparse import ArgumentParser


def get_input_data():
    parser = ArgumentParser(
        description='Запуск сайта'
    )
    parser.add_argument(
        '--path',
        help='Путь до .json файла с вашими данными',
        type=str,
        default='meta_data.json'
        )

    args = parser.parse_args()
    return args


def on_reload():
    makedirs("pages", exist_ok=True)

    with open(get_input_data().path, 'r', encoding='utf-8') as file:
        books_json = file.read()

    books = loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books_on_page = 10
    pages = list(chunked(books, books_on_page))

    pages_count = len(pages)

    for index, page_books in enumerate(pages, start=1):
        rendered_page = template.render(
            cards=page_books,
            page_number=index,
            pages_count=pages_count)
        with open(f"pages/index{index}.html", "w", encoding="utf-8") as f:
            f.write(rendered_page)
        rendered_page = template.render(
            cards=pages[0],
            page_number=1,
            pages_count=pages_count
        )
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', port=8000)


if __name__ == '__main__':
    main()
