import os
import urllib.request


def main() -> None:
    urllib.request.urlopen("http://127.0.0.1:" + os.environ["PORT"] + "/")


if __name__ == "__main__":
    main()
