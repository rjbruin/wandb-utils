"""Clean up artifacts from specified W&B project. Removes all "model" type
artifacts that are not tagged with any alias.

Usage:
    cleanup_artifacts.py <entity> <project> [--dry-run]

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
    models = list(api.artifact_type('model').collections())

    removed = {}
    desc = 'Removing models' if not args['--dry-run'] else 'Discovering models'
    for i, model in tqdm.tqdm(enumerate(models), desc=desc, total=len(models)):
        for j, version in enumerate(model.versions()):
            if version.state == 'DELETED':
                continue
            # if "latest" not in version.aliases and \
            #    "best" not in version.aliases and \
            #    "best_k" not in version.aliases:
            if len(version.aliases) == 0:
                if not args['--dry-run']:
                    version.delete(delete_aliases=True)

                if model.name not in removed:
                    removed[model.name] = 0
                removed[model.name] += 1

    if not args['--dry-run']:
        print(f"Removed model versions that were not \"latest\" or \"best\":")
    else:
        print(f"Found model versions that were not \"latest\" or \"best\":")
    for key in removed:
        print(f"  {key}: {removed[key]}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Clean up artifacts 1.0')
    main(arguments)