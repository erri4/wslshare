with open("virushash.txt", "r") as f:
    virushash = f.read().strip()

with open("antivirus.py", "r") as f:
    code = f.read()

new_code = f"VIRUS_HASH = '{virushash}'\n" + '\n'.join(code.splitlines()[1:])

with open("antivirus.py", "w") as f:
    f.write(new_code)
