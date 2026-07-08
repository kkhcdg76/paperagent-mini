import sys

from workflow import run_paper_reader


def main() -> None:
    topic = " ".join(sys.argv[1:]).strip()
    if not topic:
        topic = input("Research topic: ").strip()

    run_paper_reader(topic)
    print("Done.")


if __name__ == "__main__":
    main()
