from app import app
from ws import start_server
from func import get_ip


def refresh_ip() -> None:
    with open('static/ip.txt', 'w') as file:
        file.write(f'{get_ip()}')


def get_stored_ip() -> str:
    with open('static/ip.txt', encoding='utf8') as file:
        return file.read()


def main() -> None:
    refresh_ip()
    start_server(get_stored_ip())


if __name__ == 'main':
    main()
