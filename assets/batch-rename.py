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

def batch_rename():
    args = get_args()
    replace_map = [[item, sub(args.source, args.dist, item)] for item in os.listdir(args.folder)]
    results = [x[1] for x in replace_map]
    print('Preview:')
    for pair in replace_map:
        print(f'{pair[0]} -> {pair[1]}')
    if any(results.count(item) > 1 for item in results):
        print('Error!!!There is a file with the same name in the result. Aborting.')
        exit()
    confirm = input('Confirm?(y/N)')
    if confirm.lower() == 'y':
        for pair in replace_map:
            os.rename(
                os.path.join(args.folder, pair[0]), 
                os.path.join(args.folder, pair[1])
            )
        print('Succeed!')
    else:
        print("Nothing to do")

if __name__ == '__main__':
    batch_rename()