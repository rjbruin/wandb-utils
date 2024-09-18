"""
Clean up images from specified W&B project. Removes all logged files that
start with <file_prefix>.

Usage:
    cleanup_images.py <entity> <project> <file_prefix> [options]

Options:
    --dry-run   Don't apply changes.
"""
import wandb
import tqdm
from docopt import docopt


def main(args):
    api = wandb.Api(overrides={
        'entity': args['<entity>'],
        'project': args['<project>'],
    }, timeout=19)

    prefix = args['<file_prefix>']
    desc = f'Removing files {prefix}*' if not args['--dry-run'] else f'Discovering files {prefix}*'
    runs = api.runs(path='tudcv/vit-sensitivities')
    deleted = []
    for i, run in tqdm.tqdm(enumerate(runs), desc=desc, total=len(runs)):
        for file in run.files():
            if file.name.startswith(args['<file_prefix>']):
                deleted.append(file.name)
                if not args['--dry-run']:
                    file.delete()
        # run.update()

    if not args['--dry-run']:
        print(f"Removed {len(deleted)} files.")
    else:
        print(f"Found {len(deleted)} files.")
    # for fname in deleted:
    #     print(f"  {fname}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Clean up images 1.0')
    main(arguments)