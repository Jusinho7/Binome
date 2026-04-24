import random
from typing import Generator


PLAYERS: list[str] = ["alice", "bob", "charlie", "dylan"]
ACTIONS: list[str] = [
    "run", "jump", "eat", "sleep", "move",
    "climb", "swim", "grab", "release", "use"
]


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        name: str = random.choice(PLAYERS)
        action: str = random.choice(ACTIONS)
        yield (name, action)


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        idx: int = random.randrange(len(events))
        event: tuple[str, str] = events[idx]
        events.pop(idx)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    streamer: Generator[tuple[str, str], None, None] = gen_event()
    for i in range(1000):
        name, action = next(streamer)
        print(f"Event {i}: Player {name} did action {action}")

    event_list: list[tuple[str, str]] = [next(streamer) for _ in range(10)]
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()
