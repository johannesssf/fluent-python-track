import itertools
import time
from multiprocessing import Process, Event  # 1
from multiprocessing import synchronize  # 2
from slow import is_prime


def spin(msg: str, done: synchronize.Event) -> None:  # 3
    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break  # 5
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow() -> int:
    # time.sleep(3)
    # return 42
    return is_prime(5_000_111_000_222_021)


def supervisor() -> int:  # 1
    done = Event()  # 2
    spinner = Process(target=spin, args=("thinking!", done))  # 4
    print(f"spinner object: {spinner}")  # 5
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
