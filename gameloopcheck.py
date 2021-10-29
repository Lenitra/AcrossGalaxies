import random
import time
from datetime import datetime
import across
import string

count = 200

while 1:
    print("update captcha")
    letters = string.ascii_uppercase
    text = ''.join(random.choice(letters) for i in range(6))
    across.updatecapt(text)
    time.sleep(600)
