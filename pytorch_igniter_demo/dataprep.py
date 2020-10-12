from aws_sagemaker_remote.processing.main import ProcessingCommand
import os
import argparse
import os
import pprint
from torch import nn
from torch.utils import data
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from aws_sagemaker_remote.processing import sagemaker_processing_main
import aws_sagemaker_remote
from aws_sagemaker_remote.processing.main import ProcessingCommand
from aws_sagemaker_remote.commands import run_command


def get_dataset(path, train=True):
    os.makedirs(
        path, exist_ok=True
    )
    loader = MNIST(
        root=path, download=True,
        transform=transforms.ToTensor(),
        train=train
    )
    return loader


def get_loader(path, batch_size, train=True, shuffle=True):
    ds = get_dataset(path, train=train)
    dl = data.DataLoader(ds, shuffle=shuffle, batch_size=batch_size)
    return dl


def dataprep(args):
    output = args.output
    get_dataset(output)
    print("Downloaded MNIST dataset")


class DataprepCommand(ProcessingCommand):
    def __init__(self, env=None):
        super(DataprepCommand, self).__init__(
            help='Prepare dataset',
            script=__file__,
            main=dataprep,
            outputs={
                'output': 'output/data'
            },
            dependencies={
                # Add a module to SageMaker
                # module name: module path
                'aws_sagemaker_remote': aws_sagemaker_remote
            },
            configuration_command='pip3 install --upgrade sagemaker sagemaker-experiments',
            base_job_name='pytorch-igniter-demo-dataprep',
            env=env
        )


if __name__ == '__main__':
    command = DataprepCommand()
    run_command(
        command=command,
        description='pytorch-igniter demo dataprep'
    )
