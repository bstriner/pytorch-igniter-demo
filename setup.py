from setuptools import find_packages, setup
import os
with open(os.path.abspath(os.path.join(__file__, '../README.rst')), encoding='utf-8') as f:
    long_description = f.read()
setup(name='pytorch-igniter-demo',
      version='0.0.3',
      author='Ben Striner',
      author_email="bstriner@gmail.com",
      url='https://github.com/bstriner/pytorch-igniter-demo',
      description="Demo for pytorch-igniter",
      install_requires=[
          'pytorch-igniter==0.0.42',
          'aws-sagemaker-remote==0.0.48'
      ],
      package_data={'': [
          '**/*.txt'
      ]},
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'pytorch-igniter-demo=pytorch_igniter_demo.main:main'
          ]
      },
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type='text/x-rst')
