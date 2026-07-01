from time import sleep, time, ctime

def greet_customer(customer):
    print(f"{ctime()} Greeting for Customer-{customer}...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} Greeting for Customer-{customer}...Done!")

def take_order(customer):
    print(f"{ctime()} [Thread-{customer}] Taking Order...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Taking Order...Done!")

def do_cooking(customer):
    print(f"{ctime()} [Thread-{customer}] Cooking spaghetti...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Cooking spaghetti...Done!")

def mini_bar(customer):
    print(f"{ctime()} [Thread-{customer}] Manage Bar for Drink...")
    sleep(1)  # Simulating a time-consuming task
    print(f"{ctime()} [Thread-{customer}] Manage Bar for Drink...Done!")
    print(f"{ctime()} [Thread-{customer}] All served!\n")

if __name__ == "__main__":
    customers = ["A", "B", "C"]  # List of customers to serve
    start_time = time()

    for customer in customers:
        greet_customer(customer)
        take_order(customer)
        do_cooking(customer)
        mini_bar(customer)

    duration = time() - start_time
    print(f"{ctime()} Finished Cooking in {duration:.2f} seconds")