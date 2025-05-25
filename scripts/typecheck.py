import sys
import subprocess


def main():
    files = sys.argv[1:] or ["src/"]
    retcode = subprocess.call(["poetry", "run", "ty", "check"] + files)
    sys.exit(retcode)


if __name__ == "__main__":
    main()
