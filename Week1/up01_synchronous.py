from time import sleep, ctime, time
import os
import threading

def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | LCD: Done for customer {customer_name}!")

def make_coffee(customer_name):
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | coffee ready for {customer_name}!")

def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id
    
    print(f"{ctime()} | === Synchronous Coffee Machine ===")
    start_time = time()
    
    # ลูปทำงานตามลำดับคิวเดี่ยว (ทีละคน)
    for customer in queue:
        make_coffee(customer)
        update_cup_number(customer)
        
    duration = time() - start_time
    print(f"{ctime()} | total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    main()