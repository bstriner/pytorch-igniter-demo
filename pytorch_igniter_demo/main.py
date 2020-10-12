from pytorch_igniter.experiment_cli import experiment_cli
from pytorch_igniter_demo.config import make_config
from pytorch_igniter_demo.dataprep import DataprepCommand
import pytorch_igniter_demo

def main(dry_run=False):
    """
    Generate experiment CLI.
    Running locally, this function is run by a wrapper created by setuptools
    """
    return experiment_cli(
        config=make_config(),
        script=__file__,
        description='pytorch-igniter demo script',
        extra_commands={
            'dataprep': DataprepCommand()
        },
        model_dir='output/model',
        checkpoint_dir='output/checkpoint',
        output_dir='output/output',
        dry_run=dry_run,
        dependencies ={
            'pytorch_igniter_demo': pytorch_igniter_demo
        }
    )


def parser_for_docs():
    """
    Create a parser for generating documentation
    """
    return main(dry_run=True)


if __name__ == '__main__':
    # Running remotely, this is where execution starts
    main()
