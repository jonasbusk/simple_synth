from keyboard import Keyboard
from synth import Synth


def main():
    s = Synth(keyboard=Keyboard())
    s.start()

if __name__ == '__main__':
    main()
