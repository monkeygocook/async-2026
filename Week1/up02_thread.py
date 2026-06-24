from time import sleep, ctime, time
import threading

def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):    
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    update_cup_number(customer_name)


def main():
    queue = ['A', 'B', 'C']
    
    print(f"{ctime()} | === Multi-thread Coffee Machine ===")
    start_time = time()
    
    threads = []
    # ลูปการทำงาน Thread
    for customer in queue:
        # เราสามารถตั้งชื่อ Thread ผ่านพารามิเตอร์ name= ได้เพื่อให้ไล่โค้ดง่ายขึ้น
        t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
        #u = threading.Thread(target=update_cup_number, args=(customer,), name=f"Thread-{customer}")
        threads.append(t)
        t.start()


    for t in threads:
        t.join()

    duration = time() - start_time
    print(f"{ctime()} | total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    main()