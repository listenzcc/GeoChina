# File: main.py
# Aim: main entrance of the project

# %%
from GeoData.manager import Manager

manager = Manager()

adcode_history = [(100000, '全国')]


def main():
    adcode = 100000
    while True:
        frame = manager.fetch(adcode=adcode)
        if frame is None:
            print('???? Can not fetch data, restoring latest success')
            adcode_history.pop()
            adcode = adcode_history[-1][0]
            continue

        table = manager.get_children(frame)

        print('-----------------------------------------------')
        # List candidates
        lst = [name for name in table]
        for j, name in enumerate(lst):
            print(j, name)
        inp = input(f'{adcode_history} >> ')

        # Show frame
        if inp == 'f':
            print(frame)
            continue

        # Quit
        if inp == 'q':
            print(f'Quitting...')
            break

        # Move backward
        if inp == '..':
            if len(adcode_history) > 1:
                adcode_history.pop()
            adcode = adcode_history[-1][0]
            continue

        # Move forward
        # Try to get [idx]
        try:
            idx = int(inp)
        except ValueError:
            print(f'!!!! ValueError occurred, continuing')
            continue
        # Try to get [adcode]
        try:
            name = lst[idx]
            adcode = int(table[name][0])
            adcode_history.append((adcode, name))
            print('Selecting {}'.format(name))
        except IndexError:
            print(f'!!!! IndexError occurred, continuing')
            continue

    pass


if __name__ == '__main__':
    main()
    print('ByeBye')

# %%
