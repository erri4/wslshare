from BetterLinkedLists import *

class RotorEncryptor:
    dkey: DoubleLoopedLinkedList
    jkey: DoubleLoopedLinkedList
    wheels = []
    rotates = 0

    def __init__(self, key, *wheels):
        self.jkey, self.dkey = self.processkey(key)
        for wheel in wheels:
            self.wheels.append(DoubleLoopedLinkedList(wheel))

    def processkey(self, key: str) -> list[DoubleLoopedLinkedList]:
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

        return [DoubleLoopedLinkedList(j_values), DoubleLoopedLinkedList(d_values)]

    def findwheel(self, char):
        for wheel in self.wheels:
            if char in wheel:
                return wheel
        return None

    def rotate(self, char, de = 1):
        jkeyvalue = self.jkey[self.rotates % len(self.jkey)]
        dkeyvalue = self.dkey[self.rotates % len(self.dkey)]

        wheel = self.findwheel(char)
        if not wheel:
            return char
        self.rotates += 1

        return linkedlisttools.jump(wheel, char, jkeyvalue.data * dkeyvalue.data * de).data