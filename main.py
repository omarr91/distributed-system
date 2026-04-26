from workers.gpu_worker import GPUWorker
from lb.load_balancer import LoadBalancer
from master.scheduler import Scheduler
from client.load_generator import run_load_test


def choose_strategy():
    print("\n===== Load Balancer Menu =====")
    print("1. Round Robin")
    print("2. Least Connections")
    print("3. Load Aware")

    choice = input("Choose a strategy (1-3): ")

    if choice == "1":
        return "round_robin"
    elif choice == "2":
        return "least_connections"
    elif choice == "3":
        return "load_aware"
    else:
        print("❌ Invalid choice, defaulting to Round Robin")
        return "round_robin"


def main():
    strategy = choose_strategy()

    print(f"\n🚀 Running with strategy: {strategy}\n")

    # Create workers
    workers = [GPUWorker(i) for i in range(4)]

    # Load balancer
    lb = LoadBalancer(workers, strategy=strategy)

    # Scheduler
    scheduler = Scheduler(lb)

    # Run test
    run_load_test(scheduler, num_users=1000)

while True:
    strategy = choose_strategy()
    print(f"\n🚀 Running with strategy: {strategy}\n")

    workers = [GPUWorker(i) for i in range(4)]
    lb = LoadBalancer(workers, strategy=strategy)
    scheduler = Scheduler(lb)

    run_load_test(scheduler, num_users=1000)

    again = input("\nRun again? (y/n): ")
    if again.lower() != "y":
        break
if __name__ == "__main__":
    main()