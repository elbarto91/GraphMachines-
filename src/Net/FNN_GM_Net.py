from pathlib import Path

import torch
import torch.nn as nn


# neural network used in regression task,constructed in run-time,infact it can have any hiddetn layer's node
class RegressionGm(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RegressionGm, self).__init__()  # Inherited from the parent class nn.Module
        self.fc1 = nn.Linear(input_size, hidden_size,
                             bias=False)  # 1st Full-Connected Layer:  (input data) ->  (hidden node)
        self.fc2 = nn.Linear(hidden_size, output_size,
                             bias=False)  # 2nd Full-Connected Layer:  (hidden node) ->  (output class)
        self.Selu = nn.SELU()
        self.fc1Root = nn.Linear(input_size, hidden_size,
                                 bias=False)  # 1st Full-Connected Layer:  (input data) ->  (hidden node)
        self.fc2Root = nn.Linear(hidden_size, output_size,
                                 bias=False)  # 2nd Full-Connected Layer:  (hidden node) ->  (output class)
        self.LSeluRoot = nn.SELU()

    # in the forword we check if it is the last depth(root nodes) to use a different layer
    def forward(self, batch_tensor, depth):
        if depth == 0:
            out = self.fc1Root(batch_tensor)
            out = self.LSeluRoot(out)
            out = self.fc2Root(out)
            return out
        else:
            out = self.fc1(batch_tensor)
            out = self.Selu(out)
            out = self.fc2(out)
            return out


# neural network used in classification task,constructed in run-time,infact it can have any hiddetn layer's node
class ClassificationGm(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ClassificationGm, self).__init__()  # Inherited from the parent class nn.Module
        self.fc1 = nn.Linear(input_size, hidden_size,
                             bias=False)  # 1st Full-Connected Layer:  (input data) ->  (hidden node)
        nn.init.kaiming_normal_(self.fc1.weight)

        self.fc2 = nn.Linear(hidden_size, output_size,
                             bias=False)  # 2nd Full-Connected Layer:  (hidden node) ->  (output class)
        nn.init.kaiming_normal_(self.fc2.weight)

        self.Relu = nn.ReLU()

        self.fc1Root = nn.Linear(input_size, hidden_size,
                                 bias=False)  # 1st Full-Connected Layer:  (input data) ->  (hidden node)
        nn.init.kaiming_normal_(self.fc1Root.weight)

        self.fc2Root = nn.Linear(hidden_size, output_size,
                                 bias=False)  # 2nd Full-Connected Layer:  (hidden node) ->  (output class)
        nn.init.kaiming_normal_(self.fc2Root.weight)
        self.Drop = nn.Dropout(0.15)
        self.ReluRoot = nn.ReLU()

    # in the forword we check if it is the last depth(root nodes) to use a different layer
    def forward(self, batch_tensor, deep):
        if deep != 0:
            out = self.fc1(batch_tensor)
            out = self.Relu(out)
            out = self.Drop(out)
            out = self.fc2(out)
            return out
        else:  # root node utilized to prdict
            out = self.fc1Root(batch_tensor)
            out = self.ReluRoot(out)
            out = self.Drop(out)
            out = self.fc2Root(out)
            return out


def save_model(model, reportName, model_name):
    # use .pth or .pt extension
    Path('models/' + reportName).mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), 'models/' + reportName + model_name)


def laod_model(model, path):
    model.load_state_dict(torch.load(path))
    return model
