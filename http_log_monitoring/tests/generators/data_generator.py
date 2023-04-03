import random
import string
import time
from typing import Iterable

from dto import LogLineDto


def generate_infinite_log_file():
    """
    Generate infinite file with logs
    retrieving from another file in random order
    """
    with open("data/sample_csv_original.txt") as input_file, \
            open("data/test_csv.txt", "w", buffering=1) as output_file:
        lines = input_file.readlines()
        output_file.write(lines[0])
        lines = lines[1:]
        while True:
            line = random.choice(lines).split(',')
            line[3] = str(int(time.time()))
            output_file.write(",".join(line))
            time.sleep(random.uniform(0, 1))


def generate_n_log_lines(n: int) -> Iterable[LogLineDto]:
    log_line_dict = {'remotehost': '10.0.0.4',
                     'rfc931': '-',
                     'authuser': 'apache',
                     'date': 1549573860.0,
                     'request': 'GET /api/user HTTP/1.0',
                     'status': 200.0,
                     'bytes': 1234.0}

    for i in range(n):
        yield LogLineDto(**log_line_dict)


def generate_random_n_log_lines(n: int) -> Iterable[LogLineDto]:
    for i in range(n):
        log_line_dict = {'remotehost': random_remote_host(),
                         'rfc931': random_string(),
                         'authuser': random_string(),
                         'date': time.time(),
                         'request': random_request(),
                         'status': random_status_code(),
                         'bytes': random_bytes()}
        yield LogLineDto(**log_line_dict)


def random_remote_host():
    length = random.randrange(4, 7)
    return '.'.join(str(random.randrange(12) for _ in range(length)))


def random_request():
    method = random.choice(['POST', 'GET', 'DELETE', 'PUT'])
    protocol = "HTTP/" + str(float(random.randint(1, 5)))
    request = '/'.join(random_string() for _ in range(random.randint(1, 5)))
    if random.randrange(100) < 50:
        request = "/" + request
    return ' '.join([method, protocol, request])


def random_string():
    letters = string.ascii_lowercase
    length = random.randrange(100)
    return '.'.join(str(random.choice(letters) for _ in range(length)))


def random_bytes():
    return float(random.randrange(10000))


def random_status_code():
    return float(random.randint(100, 600))
