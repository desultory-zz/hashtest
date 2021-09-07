#!/usr/bin/env python3

import hashlib
import random
import base64
import time
from csv import DictWriter

file_name = "results.csv"
size_min = 7
size_limit = 22
ommitted_types = ['md4', 'md5', 'md5-sha1', 'mdc2', 'sha1', 'ripemd160']

def get_hash_algos():
    #gets available hash algorithms
    algos = hashlib.algorithms_available
    algos = list(algos)
    out_algos = []
    for a in algos:
        if a not in ommitted_types:
            out_algos.append(a)
    return out_algos

def make_dummy_data(size):
    data = []

    while len(data) < size:
        data.append(base64.b64encode(bytes(str(random.random()), 'utf-8')))
    
    data_str = ''

    for i in data:
        data_str += str(i)

    return data_str

def time_cipher(cipher_name, data):
    bytes_data = bytes(data, 'utf-8')
    cipher = hashlib.new(cipher_name)
    
    t = time.process_time()
    cipher.update(bytes_data)
    elapsed = time.process_time() - t
    return(elapsed)

if __name__ == '__main__':
    algos = get_hash_algos()
    header = algos.copy()
    header.append('size')
    header = tuple(header)
    results_combined = []
    
    sizes = []
    for n in range(size_min, size_limit):
        sizes.append(2**n)

    for size in sizes:
        data = make_dummy_data(size)
        results = {}
        results['size'] = size
        for a in algos:
            t = time_cipher(a, data)
            results[a] = t
        results_combined.append(results)
    
    with open(file_name, 'w') as output:
        writer = DictWriter(output, (header))
        writer.writeheader()
        writer.writerows(results_combined)


