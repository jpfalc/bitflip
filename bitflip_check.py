import os
import time
import hashlib

# settings
chunk_size = 25000000 #25 MiB chunks
num_chunks = 3000 # 75 GiB total
check_interval = 3600 # 1 hour check interval

data = []
hashes = []

# create and hash random data
print('creating and hashing', num_chunks, 'chunks of random data,', round(chunk_size/1000000), 'MiB each, total of', round(chunk_size*num_chunks/1000000), 'MiB')
for i in range(num_chunks):
    random_bytes = bytearray(os.urandom(chunk_size))
    md5 = hashlib.md5()
    md5.update(random_bytes)
    data.append(random_bytes)
    hashes.append(md5.hexdigest())
print('data and hashes created')

# validate data
check_number = 0
while 1:
    time.sleep(check_interval)
    check_number += 1
    num_errors = 0
    for i in range(num_chunks):
        md5 = hashlib.md5()
        md5.update(data[i])
        if md5.hexdigest() != hashes[i]:
            str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(str_time, 'error detected in chunk', i, ', expected', hashes[i], 'but got', md5.hexdigest())
            hashes[i] = md5.hexdigest()
            num_errors += 1
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(str_time, 'finished check number', check_number, 'with', num_errors, 'errors')
