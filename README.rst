pytorch-igniter-demo
=====================

Demo for pytorch-igniter

Local usage
++++++++++++

.. code-block:: bash

   # Local training
   pytorch-igniter-demo dataprep --output output/data
   pytorch-igniter-demo train-and-eval --input output/data

   # Local inference
   aws-sagemaker-remote endpoint invoke --model-dir output/model --input test/test-image.png --output-type application/json --output output/invoke-local.json

   # Upload local model
   aws-sagemaker-remote upload output/model pytorch-igniter-demo/model.tar.gz --gz
   aws-sagemaker-remote model create --name pytorch-igniter-demo --model-artifact pytorch-igniter-demo/model.tar.gz --force
   aws-sagemaker-remote endpoint-config create --model pytorch-igniter-demo --force
   aws-sagemaker-remote endpoint create --config pytorch-igniter-demo --force
   aws sagemaker wait endpoint-in-service --endpoint-name pytorch-igniter-demo

   # Invoke remote model
   aws-sagemaker-remote endpoint invoke --name pytorch-igniter-demo --input test/test-image.png --output output/invoke-upload.json --output-type application/json

   # Clean up resources
   aws-sagemaker-remote endpoint delete pytorch-igniter-demo
   aws-sagemaker-remote endpoint-config delete pytorch-igniter-demo
   aws-sagemaker-remote model delete pytorch-igniter-demo


Remote usage
++++++++++++

.. code-block:: bash

   # Dataprep
   pytorch-igniter-demo dataprep --sagemaker-run yes

   # Training
   pytorch-igniter-demo train-and-eval --sagemaker-run yes --input s3://sagemaker-us-east-1-683880991063/pytorch-igniter-demo-dataprep-2020-10-09-01-20-47-571/output/output

   # Deploy model
   aws-sagemaker-remote model create --name pytorch-igniter-demo --job pytorch-igniter-demo...
   aws-sagemaker-remote endpoint-config create --model pytorch-igniter-demo --force
   aws-sagemaker-remote endpoint create --config pytorch-igniter-demo --force
   aws sagemaker wait endpoint-in-service --endpoint-name pytorch-igniter-demo

   # Invoke remote model
   aws-sagemaker-remote endpoint invoke --name pytorch-igniter-demo --input test/test-image.png --output output/invoke-upload.json --output-type application/json

   # Clean up resources
   aws-sagemaker-remote endpoint delete pytorch-igniter-demo
   aws-sagemaker-remote endpoint-config delete pytorch-igniter-demo
   aws-sagemaker-remote model delete pytorch-igniter-demo

   

       
