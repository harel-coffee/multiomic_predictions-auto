#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import uuid
import json
import click
import hashlib
import subprocess
from pathlib import Path
from copy import deepcopy
import multiprocessing as mp
from sklearn.model_selection import ParameterGrid

print(__file__)
EXP_FOLDER = 'scratch/expts'


def get_hash(task):
    task = deepcopy(task)
    return hashlib.sha1(json.dumps(task, sort_keys=True).encode()).hexdigest()
 

graham_sbatch_template_multiple = r"""#!/bin/bash
#SBATCH --cpus-per-task={cpus}
#SBATCH --array={start_idx}-{end_idx}

date
SECONDS=0
which python
python3 {dispatcher_file} run-sbatch  --exp_name {exp_name} --hpid $SLURM_ARRAY_TASK_ID -e {exec_file}
diff=$SECONDS
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
date
"""

graham_sbatch_template_single = r"""#!/bin/bash
#SBATCH --cpus-per-task={cpus}

date
SECONDS=0
which python
{exec_cmd}
diff=$SECONDS
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
date
"""


aws_sbatch_template_multiple = r"""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --cpus-per-task={cpus}{gpu_entry}
#SBATCH --array={start_idx}-{end_idx}

date
SECONDS=0
which python
python3 {dispatcher_file} run-sbatch  --exp_name {exp_name} --hpid $SLURM_ARRAY_TASK_ID -e {exec_file}
diff=$SECONDS
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
date
"""

aws_sbatch_template_single = r"""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --cpus-per-task={cpus}{gpu_entry}

date
SECONDS=0
which python
{exec_cmd}
diff=$SECONDS
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
date
"""


@click.group()
def cli():
    pass


@cli.command(help="Run an experiment on single hyper-parameter config.")
@click.option('-p', '--hp_config', type=str, default=None, help="""hyper-parameter config for training""")
@click.option('-o', '--output_path', type=str, default=None, help="""output path for training result""")
def run_single_hp(hp_config, output_path):
    expt_folder = os.path.dirname(os.path.abspath(__file__))
    print(f"{expt_folder}/train_rxn_models -p {hp_config} -o {output_path}")
    process = subprocess.Popen(f"{expt_folder}/train_rxn_models -p {hp_config} -o {output_path}", shell=True)
    process.communicate()
    if process.returncode != 0:
        exit()


@cli.command(help="Run a dispatched experiment on sbatch cluster. The id of the experiment must be provided")
@click.option('-n', '--exp_name', type=str, default='test', help="Unique name for the experiment.")
@click.option('-p', '--hpid', type=int, default=0,
              help="""Position of the config file to run""")
@click.option('-e', '--exec_file', type=str, default='train',
              help=""" path to script that will be run. It is only used if instance_type is 'local'
                        and imagename is None. """)
def run_sbatch(exp_name, hpid, exec_file):
    exp_dir = os.path.join(Path.home(), EXP_FOLDER, exp_name)
    all_filenames_location = os.path.join(exp_dir, 'configs', 'configs.txt')
    with open(all_filenames_location, 'r') as fd:
        config_file = fd.readlines()[hpid].rstrip()

    print(f"{exec_file} -p {config_file} -o {exp_dir}")
    process = subprocess.Popen(f"{exec_file} -p {config_file} -o {exp_dir}", shell=True)
    process.communicate()
    if process.returncode != 0:
        exit()
    os.rename(config_file, config_file.replace('.json', '.done'))


def dispatch_sbatch(exp_name, config_file, exec_file, memory, duration, cpus, type_gpus,
                    n_gpus, account_id, partition, cluster='graham'):
    exp_dir = os.path.join(Path.home(), EXP_FOLDER, exp_name)

    config_dir = os.path.join(exp_dir, 'configs')
    os.makedirs(config_dir, exist_ok=True)

    with open(config_file, 'r') as fd:
        task_config = json.load(fd)

    task_grid = list(ParameterGrid(task_config))

    task_grid = {get_hash(task): task for task in task_grid}
    print(f"- Experiment has {len(task_grid)} different tasks:")

    existing_exp_files = [os.path.splitext(f) for f in os.listdir(os.path.join(exp_dir, 'configs'))]

    done_task_ids = [
        task_id for task_id, ext in existing_exp_files
        if (task_id in task_grid.keys() and ext == '.done')
    ]
    planned_task_ids = [
        task_id for task_id, ext in existing_exp_files if
        (task_id in task_grid.keys() and ext == '.json')
    ]
    new_task_ids = [
        task_id for task_id in task_grid
        if task_id not in done_task_ids + planned_task_ids
    ]

    if new_task_ids:
        print(f'\nNew:', *new_task_ids, sep='\n')
    if planned_task_ids:
        print('\nPlanned:', *planned_task_ids, sep='\n')
    if done_task_ids:
        print('\nCompleted:', *done_task_ids, sep='\n')

    print(f"\n\t*New: {len(new_task_ids)}\n"
          f"\t*Planned: {len(planned_task_ids)}\n"
          f"\t*Completed: {len(done_task_ids)}\n")

    planned_as_well = len(planned_task_ids) == 0 \
                      or input('>> Relaunch already planned tasks ? [N/y]').lower() in {'y', 'yes'}

    tasks = new_task_ids + planned_task_ids if planned_as_well else new_task_ids

    # Uploading on the exp folder
    all_filenames = []
    for task_id in tasks:
        fname = os.path.join(config_dir, f"{task_id}.json")
        with open(fname, 'w') as f:
            json.dump(task_grid[task_id], f)
        all_filenames.append(fname)
    all_filenames_location = os.path.join(config_dir, 'configs.txt')
    if os.path.exists(all_filenames_location):
        with open(all_filenames_location, 'r') as fd:
            start_idx = len(fd.readlines())
    else:
        start_idx = 0
    with open(all_filenames_location, 'a') as fd:
        fd.writelines([el + '\n' for el in all_filenames])
    end_idx = start_idx + len(all_filenames)

    dispatcher_file = os.path.abspath(__file__)
    gpu_entry = f'\n#SBATCH --gres=gpu:{type_gpus}:{n_gpus}' if n_gpus > 0 else ""
    template_args = dict(start_idx=start_idx, end_idx=end_idx - 1,
                         exp_name=exp_name, exec_file=exec_file,
                         duration=duration, cpus=cpus, memory=memory, gpu_entry=gpu_entry,
                         dispatcher_file=dispatcher_file, account_id=account_id, partition=partition)
    if cluster.lower() == 'graham':
        sbatch_script = graham_sbatch_template_multiple.format(**template_args)
    elif cluster.lower() == 'aws':
        sbatch_script = aws_sbatch_template_multiple.format(**template_args)
    else:
        raise Exception("Unknown cluster")
    sbatch_script_location = os.path.join(exp_dir, 'submit.sh')
    with open(sbatch_script_location, 'w') as fd:
        fd.write(sbatch_script)

    print(sbatch_script)
    os.chdir(exp_dir)
    process = subprocess.Popen(f"sbatch {sbatch_script_location} -D {exp_dir}", shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stdout)
        print(stderr)


def dispatch_local(config_file, exec_file, outpath):
    with open(config_file, 'r') as fd:
        config = json.load(fd)

    hp_grid = list(ParameterGrid(config))

    print("Quick summary")
    print(f"Number of tasks: {len(hp_grid)}")

    for i, hp in enumerate(hp_grid):
        config_dir = os.path.dirname(os.path.abspath(
            os.path.expandvars(config_file)))
        local_cfg_file = os.path.join(config_dir, f"temp_{str(uuid.uuid4())}.json")
        try:
            with open(local_cfg_file, 'w') as fp:
                json.dump(hp, fp)
            print(f"Executing ... \n>>> python3 {exec_file} -p {local_cfg_file} -o {outpath}")
            process = subprocess.Popen(f"python3 {exec_file} -p {local_cfg_file} -o {outpath}", shell=True)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                exit(44)
        except:
            exit(44)
        finally:
            os.remove(local_cfg_file)


@cli.command(help="Run a dispatched experiment on sbatch cluster. The name of the experiment must be provided")
@click.option('--exp-name', type=str, default='test', help="Unique name for the experiment.")
@click.option('--server', type=str, default='local',
              help=""" server where the experiments is running: local | graham | aws. """)
@click.option('--config-file', type=str, default=None,
              help="""The name/path of the config file (in json format) that contains all the parameters for
                    the experiment. This config file should be at the same location as the train file""")
@click.option('--output-path', type=str, default='./results/local_runs', help="""The outpath""")
@click.option('--duration', type=str, default='02:00:00',
              help="""Duration of each task in the experiment. Will only be used on clusters with schedulers""")
@click.option('--cpus', type=int, default=8,
              help="""Number of cpus per task""")
@click.option('--memory', type=str, default="16G",
              help="""Number of cpus per task""")
@click.option('--n_gpus', type=int, default=0,
              help="""Number of cpus per task""")
@click.option('--type_gpus', type=str, default='t4',
              help="""type of gpu used in this expt""")
@click.option('--partition', type=str, default="general",
              help="""Partition name """)
@click.option('--account_id', type=str, default="rrg-corbeilj-ac",
              help="""Number of cpus per task""")
def dispatch(exp_name, server, config_file, output_path, duration, cpus, memory,
             n_gpus, type_gpus, partition, account_id):
    expt_folder = os.path.dirname(os.path.abspath(__file__))

    if config_file is None:
        config_file = os.path.join(expt_folder, "config.json")

    if not os.path.exists(config_file):
        raise Exception("We were expecting an existing config file or a config.json in "
                        "the experiment folder but none were given")

    if server == "local":
        dispatch_local(
            config_file=config_file,
            exec_file=f"{expt_folder}/train_rxn_models", outpath=output_path)
    else:
        dispatch_sbatch(
            exp_name=exp_name,
            config_file=config_file,
            exec_file=f"{expt_folder}/train_rxn_models",
            memory=memory, duration=duration, cpus=cpus, n_gpus=n_gpus,
            type_gpus=type_gpus, account_id=account_id, partition=partition, cluster=server)


@cli.command(help="Run a script on sbatch cluster.")
@click.option('--ename', type=str, default='test', help="Unique name for the experiment.")
@click.option('--cmd', '-c', type=str, default='test', help="command to run.")
@click.option('--duration', type=str, default='12:00:00',
              help="""Duration of each task in the experiment. Will only be used on clusters with schedulers""")
@click.option('--cpus', type=int, default=16,
              help="""Number of cpus per task""")
@click.option('--n_gpus', type=int, default=0,
              help="""Number of cpus per task""")
@click.option('--type_gpus', type=str, default='t4',
              help="""type of gpu used in this expt""")
@click.option('--memory', type=str, default="32G",
              help="""Number of cpus per task""")
@click.option('--account_id', type=str, default="rrg-corbeilj-ac",
              help="""Number of cpus per task""")
@click.option('--cluster', type=str, default="graham",
              help="""Name of the cluster: aws gpc or graham""")
def submit_sbatch(ename, cmd, duration, cpus, type_gpus, n_gpus, memory, account_id, cluster):
    gpu_entry = f'\n#SBATCH --gres=gpu:{type_gpus}:{n_gpus}' if n_gpus > 0 else ""
    template_args = dict(exec_cmd=cmd, duration=duration, cpus=cpus,
                         memory=memory, account_id=account_id, gpu_entry=gpu_entry)
    if cluster.lower() == 'graham':
        sbatch_script = graham_sbatch_template_single.format(**template_args)
    elif cluster.lower() == 'aws':
        sbatch_script = aws_sbatch_template_single.format(**template_args)
    else:
        raise Exception("Unknown cluster")

    sbatch_script_location = f'{ename}_submit.sh'
    with open(sbatch_script_location, 'w') as fd:
        fd.write(sbatch_script)

    print(sbatch_script)
    process = subprocess.Popen(f"sbatch {sbatch_script_location}", shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stdout)
        print(stderr)


if __name__ == '__main__':
    mp.set_start_method('spawn')
    cli()