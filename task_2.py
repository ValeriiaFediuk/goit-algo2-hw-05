import json
import time
from datasketch import HyperLogLog

hll = HyperLogLog(p=15)

def read_logs():
    ip_lst = []
    with open("lms-stage-access.log") as file:
        for line in file:
            try:
                data = json.loads(line)
                ip = data.get("remote_addr")
                if ip:
                    update_hll(ip)
                    ip_lst.append(ip)
            except json.JSONDecodeError:
                continue
    return ip_lst

def update_hll(ip):
    hll.update(ip.encode("utf-8"))

def hll_count():
    return hll.count()

def set_count(ip_lst):
    return len(set(ip_lst))

def timer(func, *args):
    start_time = time.time()
    res = func(*args)
    time_diff = time.time() - start_time
    return res, time_diff

if __name__ == "__main__":
    ip_address = read_logs()
    hll_result, hll_time = timer(hll_count)
    set_result, set_time = timer(set_count, ip_address)

    print(f"{'Method':<20}{'Unique Elements':<20}{'Time (seconds)'}")
    print("-" * 50)
    print(f"{'HyperLogLog':<20}{hll_result:<20}{hll_time:.8f}")
    print(f"{'Exact count (set)':<20}{set_result:<20}{set_time:.8f}")
