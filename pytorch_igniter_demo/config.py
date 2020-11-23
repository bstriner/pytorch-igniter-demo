from pytorch_igniter.config import IgniterConfig
from torchvision.models.resnet import resnet18
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from .dataprep import get_loader
from torch import nn
import torch.nn.functional as F
import torch
import pytorch_igniter_demo
import os
from pytorch_igniter.spec import InferenceSpec, RunSpec
from pytorch_igniter.inference.greyscale_image_input_fn import input_fn
import pytorch_igniter
import aws_sagemaker_remote

def model_args(parser):
    parser.add_argument('--classes', type=int, default=10)


def train_args(parser):
    parser.add_argument('--learning-rate', type=float, default=1e-3)
    parser.add_argument('--weight-decay', type=float, default=1e-5)
    parser.add_argument('--train-batch-size', type=int, default=32)


def eval_args(parser):
    parser.add_argument('--eval-batch-size', type=int, default=32)


class Net(nn.Module):
    def __init__(self, args):
        print("args.device: {}".format(args.device))
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


class Trainer(nn.Module):
    def __init__(self, args, model):
        super(Trainer, self).__init__()
        self.optimizer = Adam(
            params=model.parameters(),
            lr=args.learning_rate
        )
        self.criteria = CrossEntropyLoss()
        self.model = model
        metrics = {
            'loss': 'loss',
            'accuracy': 'accuracy'
        }
        loader = get_loader(
            path=args.input,
            batch_size=args.train_batch_size,
            train=True
        )
        self.spec = RunSpec(
            loader=loader,
            metrics=metrics,
            step=self.step
        )

    def step(self, engine, batch):
        self.model.train()
        self.model.zero_grad()
        x, y = batch
        yp = self.model(x)
        loss = self.criteria(input=yp, target=y)
        loss.backward()
        self.optimizer.step()
        pred = torch.argmax(yp, dim=-1)
        accuracy = torch.eq(y, pred).float().mean()
        return {
            'loss': loss,
            'accuracy': accuracy
        }


class Evaluator(object):
    def __init__(self, args, model):
        self.model = model
        self.criteria = CrossEntropyLoss()
        metrics = {
            'loss': 'loss',
            'accuracy': 'accuracy'
        }
        loader = get_loader(
            path=args.input,
            batch_size=args.eval_batch_size,
            train=False
        )
        self.spec = RunSpec(
            loader=loader,
            metrics=metrics,
            step=self.step
        )

    def step(self, engine, batch):
        #print("Step Batch: {}".format(batch))
        self.model.eval()
        x, y = batch
        yp = self.model(x)
        loss = self.criteria(input=yp, target=y)
        pred = torch.argmax(yp, dim=-1)
        accuracy = torch.eq(y, pred).float().mean()
        return {
            'loss': loss,
            'accuracy': accuracy
        }


class Inferencer(object):
    def __init__(self, args):
        self.args = args
        self.model = Net(args)
        self.model.eval()

    def inference(self, data):
        data = data.unsqueeze(0)
        output = self.model(data)
        output = output.squeeze(0)
        pred = torch.argmax(output)
        return {
            "class": pred.item(),
            "logits": output
        }


def make_config():
    return IgniterConfig(
        model_args=model_args,
        train_args=train_args,
        eval_args=eval_args,
        train_inputs={
            'input': 'output/data'
        },
        eval_inputs={
            'input': 'output/data'
        },
        make_model=Net,
        make_trainer=Trainer,
        make_evaluator=Evaluator,
        inference_spec=InferenceSpec(
            dependencies=[
                pytorch_igniter_demo
            ],
            requirements=os.path.abspath(
                os.path.join(__file__, '../inference_requirements.txt')
            ),
            inferencer=Inferencer,
            input_fn=input_fn
        ),
        max_epochs=5
    )
