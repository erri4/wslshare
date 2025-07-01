from BetterLinkedLists import *
import string
import sys

letters = DoubleLoopedLinkedList(list(string.ascii_lowercase))


def processkey(key: str) -> list[list[int]]:
    parts = key.split('d:')
    j_part = parts[0].replace('j:', '').strip()
    d_part = parts[1].strip() if len(parts) > 1 else ''

    j_values = [int(x.strip()) for x in j_part.split(',') if x.strip()]

    d_values = []
    for x in d_part.split(','):
        x = x.strip().lower()
        if x == 'up':
            d_values.append(1)
        elif x == 'down':
            d_values.append(-1)

    return [j_values, d_values]


if __name__ == '__main__':
    decode = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '--decode':
            decode = True
    key = input('key: ')
    text = input('text: ')
    jkey = DoubleLoopedLinkedList(processkey(key)[0])
    dkey = DoubleLoopedLinkedList(processkey(key)[1])
    jkeyvalue = jkey.head
    dkeyvalue = dkey.head
    text = list(text.lower())

    for i in range(len(text)):
        text[i] = linkedlisttools.jump(letters, text[i],  (-1 if decode else 1) * jkeyvalue.data * dkeyvalue.data).data if text[i] in string.ascii_lowercase else text[i]
        jkeyvalue = jkeyvalue.next
        dkeyvalue = dkeyvalue.next

    text = ''.join(text)
    print(text)
