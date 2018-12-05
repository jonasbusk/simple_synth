from keyboard import Keyboard
from synth import Synth


def main():

    kb = Keyboard()
    s = Synth()

    while True:
        key = kb.get_key()
        s.play_note(key)

    kb.terminate()
    s.terminate()

if __name__ == '__main__':
    main()
