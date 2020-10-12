CLI
========

Installing the package will install the command-line script ``pytorch-igniter-demo`` 

Features
+++++++++

* Run training, dataprep, evaluation and inference locally or on AWS servers
* Model package is self-contained with all dependencies and configuration
* Integrate with `pytorch-igniter <https://pytorch-igniter.readthedocs.io/en/latest/>`_ for creating an experiment CLI and managing training.
* Integrate with `MLflow <https://mlflow.org/>`_ for tracking training runs, including hyperparameters and metrics.
* Integrate with AWS SageMaker using `aws-sagemaker-remote <https://aws-sagemaker-remote.readthedocs.io/en/latest/>`_
  for tracking training runs and executing training remotely on managed containers.

Command-Line Arguments
++++++++++++++++++++++

Set of arguments and defaults is configured through code. See ``pytorch-igniter`` documentation.

.. argparse::
   :module: pytorch_igniter_demo.main
   :func: parser_for_docs
   :prog: pytorch-igniter-demo

See ``pytorch-igniter`` documentation for detailed option documentation.
See ``aws-sagemaker-remote`` documentation for detailed SageMaker option documentation.
