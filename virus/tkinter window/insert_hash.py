import hashlib


with open("antivirus.py", "r") as f:
    code = f.read()

line = f"VIRUS_HASH = '{hashlib.sha256(open('exe/virabot.exe', 'rb').read()).hexdigest()}'"

newcode = code.splitlines()
newcode[0] = line

with open("antivirus_temp.py", "w") as f:
    f.write('\n'.join(newcode))
