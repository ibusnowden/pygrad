#i!/usr/bin/env python
import numpy as np
from tensor import Tensor
from tqdm import tqdm
 
# load the mnist dataset

def fetch(url):
  import requests, gzip, os, hashlib, numpy
  fp = os.path.join("/tmp", hashlib.md5(url.encode('utf-8')).hexdigest())
  if os.path.isfile(fp):
    with open(fp, "rb") as f:
      dat = f.read()
  else:
    with open(fp, "wb") as f:
      dat = requests.get(url).content
      f.write(dat)
  return numpy.frombuffer(gzip.decompress(dat), dtype=np.uint8).copy()
X_train = fetch("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28))
Y_train = fetch("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz")[8:]
X_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28))
Y_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz")[8:]

# train a model

def layer(m, h):
    ret = np.random.uniform(-1., 1., size=(m, h))/np.sqrt(m*h)
    return ret.astype(np.float32)

class NewNet:
    def __init__(self):
        self.l1 = Tensor(layer(784, 128))
        self.l2 = Tensor(layer(128, 10))
        self.lr = lr

    def forward(self, x):
        return x.dot(self.l1).relu().dot(self.l2).logsoftmax()

# optimizer
class SGD:
    def __init__(self, tensors, lr):
        self.tensors = tensors

    def step():
        for t in self.tensors:
            t.data -= self.lr * t.grad

model = NewNet()
optim = SGD([model.l1, model.l2])

lr = 0.01
BS = 128
losses, accuracies = [], []
#for i in (t := trange(1000)):
for i in tqdm(range(1000)):
    samp = np.random.randint(0, X_train.shape[0], size=(BS))

    x = Tensor(X_train[samp].reshape((-1, 28*28)))
    Y = Y_train[samp]
    y = np.zeros((len(samp),10), np.float32)
    y[range(y.shape[0]), Y] = -1.0
    y = Tensor(y)

    # network
    outs = model.forward(x)

    # NLL loss function
    loss = outs.mul(y).mean()
    loss.backward()
    optim.step()

    cat = np.argmax(outs.data, axis=1)
    accuracy = (cat == Y).mean()

    # SGD
    #model.l1.data = model.l1.data - lr*model.l1.grad
    #model.l1.data = model.l2.data - lr*model.l2.grad

    # printing 
    loss = loss.data()
    losses.append(loss)
    accuracies.append(accuracy)
    #t.set_description("loss %.2f accuracy % .2f" % (loss, accuracy))
    set_description("loss %.2f accuracy % .2f" % (loss, accuracy))
# evaluate
def numpy_eval():
    Y_test_preds_out = model.forward(Tensor(X_test.reshape((-1, 28*28))))









































