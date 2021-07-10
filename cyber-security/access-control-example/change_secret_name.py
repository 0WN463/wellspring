import os
import sys
import re

SECRET_FILE = 'secret_names.txt'

with open(SECRET_FILE, 'r') as f:
    data = f.read()

user = os.getenv('USER')
new_secret = sys.argv[1]

print(f'{user} is changing their secret name to {new_secret}')

new_data = re.sub(rf'{user}\t.*', rf'{user}\t{new_secret}', data)

with open(SECRET_FILE, 'w') as f:
    f.write(new_data)
