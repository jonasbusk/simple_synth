from keyboard import Keyboard
from synth import Synth


def main():

    kb = Keyboard()
    s = Synth()

    while True:
        key = kb.get_key()
        if key is not None:
            s.play_note(60 + key)

    kb.terminate()
    s.terminate()

if __name__ == '__main__':
    main()
