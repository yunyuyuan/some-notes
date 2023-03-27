import argparse
from re import sub
import os

def get_args():
    parser = argparse.ArgumentParser(
                    prog = 'Batch Rename',
                    epilog = '')
    parser.add_argument('-f', '--folder', required=True)
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-d', '--dist', required=True)
    args = parser.parse_args()
    return args

def batch_rename(source, dist, files):
    replace_map = [item for item in ([item, sub(source, dist, item)] for item in files) if item[0] != item[1]]
    results = [x[1] for x in replace_map]
    print('Preview:')
    for pair in replace_map:
        print(f'{pair[0]} -> {pair[1]}')
    if any(results.count(item) > 1 for item in results):
        print('Error!!!There is a file with the same name in the result. Aborting.')
        exit()
    confirm = input('Confirm?(y/N)')
    if confirm.lower() == 'y':
        return replace_map
    return []

if __name__ == '__main__':
    args = get_args()
    files = os.listdir(args.folder)
    replace_map = batch_rename(args.source, args.dist, files)
    if replace_map:
        for pair in replace_map:
            os.rename(
                os.path.join(args.folder, pair[0]), 
                os.path.join(args.folder, pair[1])
            )
        print('Succeed!')
    else:
        print("Nothing to do")