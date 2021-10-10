import random
import time
from datetime import datetime
import across
import string

count = 200

while 1:
    print("update")
    across.updateallplanets()
    time.sleep(3)
    count += 1
    if count >= 200:
        letters = string.ascii_uppercase
        text = ''.join(random.choice(letters) for i in range(6))
        count = 0
        across.updatecapt(text)
