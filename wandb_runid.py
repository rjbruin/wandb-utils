"""
Extract W&B run identifiers from logs.

Usage: python3 wandb_runid.py <slurm_jobid1> <slurm_jobid2> ...

Recommended setup: install as alias into .bashrc:
`alias wandb_id="python3 ~/wandb_runid.py "`, then call as
`wandb_id <slurm_jobid1> <slurm_jobid2> ...` to get a W&B run ID on each line,
to be piped into other commands.
"""
#!/usr/bin/env python3
import os
import argparse

# TODO: change this to the path where you store your slurm logs
base_path = '~/out'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('slurm_id', type=int, nargs='+')
    args = parser.parse_args()

    # Read all lines at ~/bulk-home/outs/run-<slurm_id>.out
    for slurm_id in args.slurm_id:
        with open(os.path.join(base_path, f'run-{slurm_id}.out'), 'rb') as f:
            lines = [line.decode('unicode_escape') for line in f.readlines()]
            for line in lines:
                if "View run at" in line:
                    wandb_id = line.strip().split('/')[-1]
                    print(wandb_id)
                    break
