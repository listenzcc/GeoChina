# File: main.py
# Aim: main entrance of the project

# %%
from GeoData.manager import Manager

manager = Manager()


def main():
    adcode_history = [(100000, '全国')]
    adcode = 100000
    while True:
        geojson, geodf = manager.fetch(adcode=adcode)
        if geojson is None:
            print('???? Can not fetch data, restoring latest success')
            adcode_history.pop()
            adcode = adcode_history[-1][0]
            continue

        print('-----------------------------------------------')
        # List candidates
        print(geodf[['adcode', 'level', 'parent', 'center', 'childrenNum']])
        inp = input(f'{adcode_history} >> ')

        # Show frame
        if inp == 'f':
            print(geodf[['adcode', 'level', 'parent', 'center', 'childrenNum']])
            continue

        # Draw map
        if inp == 'd':
            fig = manager.draw_latest()
            fig.show()
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

        # Try to get [adcode],
        # check and select idx
        if idx not in range(0, len(geodf)):
            print(f'!!!! IndexError occurred, continuing')
            continue

        name = geodf.index[idx]
        adcode = int(geodf.loc[name]['adcode'])
        adcode_history.append((adcode, name))
        print('Selecting {}'.format((adcode, name)))


if __name__ == '__main__':
    main()
    print('ByeBye')

# %%
