from os import PathLike

ALL = None


def hide(data: str, path: PathLike, marker = b'<<<HIDDEN>>>'):
    with open(path, 'ab') as f:
        f.write(marker + data.encode())


def reveal(path: PathLike, marker: bytes = b'<<<HIDDEN>>>') -> list[str]:
    with open(path, 'rb') as f:
        content = f.read()
    parts = content.split(marker)[1:]
    return [part.decode(errors='ignore') for part in parts]


def delete(path: PathLike, amount: int | None = ALL, marker: bytes = b'<<<HIDDEN>>>'):
    with open(path, 'rb') as f:
        content = f.read()

    parts = content.split(marker)

    if len(parts) == 1:
        return

    messages = parts[1:]

    if amount is None or amount >= len(messages):
        new_content = parts[0]
    else:
        new_messages = messages[:-amount]
        new_content = parts[0] + b''.join(marker + m for m in new_messages)

    with open(path, 'wb') as f:
        f.write(new_content)


delete('space.png')
hide('hello there', 'space.png')
print(reveal('space.png'))
delete('space.png')
hide('hello there', 'space.png')
hide('hello there', 'space.png')
print(reveal('space.png'))
delete('space.png', 1)
print(reveal('space.png'))