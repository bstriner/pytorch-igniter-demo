pytorch-igniter-demo
=====================

Demo for `pytorch-igniter <https://pytorch-igniter.readthedocs.io/>`_

* Write functions for creating a model, evaluation steps and training steps
* ``pytorch-igniter`` generates a CLI for training, evaluation and inference
* Logging, checkpointing, iterating, and other features handled automatically
* Training generates a self-contained model package that can run inference

Installation
++++++++++++++

.. code-block:: bash

  pip install git+https://github.com/bstriner/pytorch-igniter-demo.git

Documentation
+++++++++++++++

View latest documentation at `ReadTheDocs <https://pytorch-igniter-demo.readthedocs.io/>`_


GitHub
+++++++++

View source code on `GitHub <https://github.com/bstriner/pytorch-igniter-demo>`_

Training and Inference
++++++++++++++++++++++

Training generates self-contained models:

* Local training generates a directory
* SageMaker training automatically gzips that directory and uploads to S3

A training package can be run locally using sagemaker libraries or uploaded to SageMaker to run remotely.

* Model data like the neural network are stored in the gz
* Directory ``code`` within the gz

   + Placed on PYTHONPATH
   + If it contains ``requirements.txt`` it is installed
   + Module ``inference`` defines inference
   + Depenencies are automatically uploaded
   + Script copies its own source to ``code`` when saving a model

The inference module defines how inference happens

* ``model_fn`` loads your model when the endpoint starts
* ``input_fn`` reads WAV, JPG, etc content from an HTTP request based on ``Content-Type`` headers
* ``predict_fn`` runs your model
* ``output_fn`` maps your predictions to HTTP responses based on ``Accept`` headers

The model directory and inference module are created automatically based on an ``InferenceSpec`` that you define

Locally or remotely trained models can be deployed locally or remotely.

Use models by posting a file in an HTTP request with appropriate ``Content-Type`` and ``Accept`` headers.

Local usage
----------------

.. code-block:: bash

   # Local dataprep
   pytorch-igniter-demo dataprep --output output/data

   # Local training
   pytorch-igniter-demo train-and-eval --input output/data

   # Invoke local model
   # Contents of directory is same as model.gz used for remote invocation
   aws-sagemaker-remote endpoint invoke --model-dir output/model --input test/test-image.png --output-type application/json --output output/invoke-local.json

   # Upload local model directory as a gzip
   # If already gzipped, skip -gz flag
   aws-sagemaker-remote upload output/model pytorch-igniter-demo/model.tar.gz --gz
   # Register SageMaker model from artifact
   aws-sagemaker-remote model create --name pytorch-igniter-demo-local --model-artifact pytorch-igniter-demo/model.tar.gz --force
   # Create endpoint configuration
   aws-sagemaker-remote endpoint-config create --model pytorch-igniter-demo-local --force
   # Create endpoint
   # This launches servers, takes a while, and begins ongoing costs
   aws-sagemaker-remote endpoint create --config pytorch-igniter-demo-local --force
   # Wait for the launch
   aws sagemaker wait endpoint-in-service --endpoint-name pytorch-igniter-demo-local

   # Invoke remote model
   # Prefer using boto3 or other libraries to invoke endpoints directly in your own code
   aws-sagemaker-remote endpoint invoke --name pytorch-igniter-demo-local --input test/test-image.png --output output/invoke-upload.json --output-type application/json

   # Clean up resources
   # Only the endpoint itself incurs any significant charges
   aws-sagemaker-remote endpoint delete pytorch-igniter-demo-local
   aws-sagemaker-remote endpoint-config delete pytorch-igniter-demo-local
   aws-sagemaker-remote model delete pytorch-igniter-demo-local


Remote usage
---------------

.. code-block:: bash

   # AWS profile
   # Run `aws configure` to configure default profile
   # Run `aws configure --profile [profile]` to configure named profile
   # Add `--sagemaker-profile [profile]` (for `pytorch-igniter-demo` command) or `--profile [profile]` (for `aws-sagemaker-remote` command) if not using default profile

   # Dataprep
   pytorch-igniter-demo dataprep --sagemaker-run yes --sagemaker-output-json output/dataprep.json

   # Training
   pytorch-igniter-demo train-and-eval --sagemaker-run yes --input json://output/dataprep.json#ProcessingOutputConfig.Outputs.output.S3Output.S3Uri --sagemaker-output-json output/training.json

   # Deploy model
   aws-sagemaker-remote model create --name pytorch-igniter-demo-remote --job json://output/training.json#TrainingJobName --force
   aws-sagemaker-remote endpoint-config create --model pytorch-igniter-demo-remote --force
   aws-sagemaker-remote endpoint create --config pytorch-igniter-demo-remote --force
   aws sagemaker wait endpoint-in-service --endpoint-name pytorch-igniter-demo-remote

   # Invoke remote model
   aws-sagemaker-remote endpoint invoke --name pytorch-igniter-demo-remote --input test/test-image.png --output output/invoke-upload.json --output-type application/json

   # Clean up resources
   aws-sagemaker-remote endpoint delete pytorch-igniter-demo-remote
   aws-sagemaker-remote endpoint-config delete pytorch-igniter-demo-remote
   aws-sagemaker-remote model delete pytorch-igniter-demo-remote


Other things
---------------

.. code-block:: bash

   # Dataprep help
   pytorch-igniter-demo dataprep --help

   # Training help
   pytorch-igniter-demo train-and-eval --help

   # Print fields from processing job JSON
   aws-sagemaker-remote json read output/dataprep.json ProcessingOutputConfig.Outputs.output.S3Output.S3Uri

   # Print fields from processing job from server
   # Get name from JSON
   aws-sagemaker-remote processing describe json://output/dataprep.json#ProcessingJobName ProcessingJobStatus
   # Pass name on command line
   aws-sagemaker-remote processing describe my-job-12345 ProcessingJobStatus

   # Print fields from training job JSON
   aws-sagemaker-remote json read output/training.json TrainingJobName

   # Print fields from training job from server
   aws-sagemaker-remote training describe json://output/training.json#TrainingJobName TrainingJobStatus
   aws-sagemaker-remote training describe json://output/training.json#TrainingJobName ModelArtifacts.S3ModelArtifacts
   
   # Check documentation on arguments to do things like change the instance, set runtime, etc.
   # * ml.c5.xlarge
   # * ml.p2.xlarge
   # * ml.g4dn.xlarge
   pytorch-igniter-demo train-and-eval \
      --sagemaker-run yes \
      --sagemaker-training-instance ml.c5.xlarge \
      --input json://output/dataprep.json#ProcessingOutputConfig.Outputs.output.S3Output.S3Uri \
      --output-json output/training.json
