import random
import time

with open("data/sample_csv_original.txt") as input_file, open("data/test_csv.txt", "w", buffering=1) as output_file:
    lines = input_file.readlines()
    output_file.write(lines[0])
    lines = lines[1:]
    while True:
        line = random.choice(lines).split(',')
        line[3] = str(int(time.time()))
        output_file.write(",".join(line))
        time.sleep(random.uniform(0, 1))
