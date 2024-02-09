import itertools
import time
from threading import Thread, Event
from slow import is_prime


def spin(msg: str, done: Event) -> None:  # 1
    for char in itertools.cycle(r"\|/-"):  # 2
        status = f"\r{char} {msg}"  # 3
        print(status, end="", flush=True)
        if done.wait(0.1):  # 4
            break  # 5
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")  # 6


def slow() -> int:
    # time.sleep(3)  # 7
    # return 42
    return is_prime(5_000_111_000_222_021)


def supervisor() -> int:  # 1
    done = Event()  # 2
    spinner = Thread(target=spin, args=("thinking!", done))  # 3
    print(f"spinner object: {spinner}")  # 4
    spinner.start()  # 5
    result = slow()  # 6
    done.set()  # 7
    spinner.join()  # 8
    return result


def main() -> None:
    result = supervisor()  # 9
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
