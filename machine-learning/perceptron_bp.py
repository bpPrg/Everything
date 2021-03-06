#!python
# -*- coding: utf-8 -*-#
"""
Perceptron Algorithm.

@author: Bhishan Poudel

@date:  Oct 31, 2017

@email: bhishanpdl@gmail.com

"""
# Imports
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import os, shutil
np.random.seed(100)

def read_data(infile):
    data = np.loadtxt(infile)
    X = data[:,:-1]
    Y = data[:,-1]
    
    # add bias to X's first column
    ones = np.ones(X.shape[0]).reshape(X.shape[0],1)
    X1 = np.append(ones, X, axis=1)
    
    return X, X1, Y

def plot_boundary(X,Y,w,epoch):
    try:
        plt.style.use('seaborn-darkgrid')
        # plt.style.use('ggplot')
        #plt.style.available
    except:
        pass
    
    # Get data for two classes
    idx0 = np.where(np.array(Y)==-1)
    idx1 = np.where(np.array(Y)==1)
    X0 = X[idx0]
    X1 = X[idx1]
           
    # plot two classes
    plt.scatter(X0[:,0],X0[:,1],c='r', marker='_', label="Negative class")
    plt.scatter(X1[:,0],X1[:,1],c='b', marker='+', label="Positive class")
    # plt.plot(X0[:,0],X0[:,1],'rD', markersize=8, label="Positive class")
    # plt.plot(X1[:,0],X1[:,1],'bo', markersize=8, label="Negative class")
    plt.title("Perceptron Algorithm iteration: {}".format(epoch))
    
    # plot decision boundary orthogonal to w
    # w is w2,w1, w0  last term is bias.
    if len(w) == 3:
        a  = -w[0] / w[1]
        b  = -w[0] / w[2]
        xx = [ 0, a]
        yy = [b, 0]
        plt.plot(xx,yy,'--g',label='Decision Boundary')
        
    if len(w) == 2:
        x2=[w[0],w[1],-w[1],w[0]]
        x3=[w[0],w[1],w[1],-w[0]]

        x2x3 =np.array([x2,x3])
        XX,YY,U,V = list(zip(*x2x3))
        ax = plt.gca()
        ax.quiver(XX,YY,U,V,scale=1, color='g')
    
    # Add labels
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # limits
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    plt.xlim(x_min,x_max)
    plt.ylim(y_min,y_max)
    
    # lines from origin
    plt.axhline(y=0, color='k', linestyle='--',alpha=0.2)
    plt.axvline(x=0, color='k', linestyle='--',alpha=0.2)
    plt.grid(True)
    plt.legend(loc=1)
    plt.show()
    plt.savefig('img/iter_{:03d}'.format(int(epoch)))
    
    # Always clost the plot
    plt.close()


def predict(X,w):
    return np.sign(np.dot(X, w))

def plot_contour(X,Y,w,mesh_stepsize):
    
    # Get data for two classes
    idx0 = np.where(np.array(Y)==-1)
    idx1 = np.where(np.array(Y)==1)
    X0 = X[idx0]
    X1 = X[idx1]
           
    # plot two classes with + and - signs
    fig, ax = plt.subplots()
    ax.set_title('Perceptron Algorithm')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(X0[:,0],X0[:,1],'rD', markersize=8, label="Positive class")
    plt.plot(X1[:,0],X1[:,1],'bo', markersize=8, label="Negative class")
    plt.legend()
      
    # create a mesh for contour plot
    # We first make a meshgrid (rectangle full of pts) from x,y min-max values.
    # We then predict the label for each grid point, and give each grid point
    # a  color according to its label.
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_stepsize),
                         np.arange(y_min, y_max, mesh_stepsize))
    
    # Get 1d array for x and y
    xxr = xx.ravel()
    yyr = yy.ravel()
    
    # column vector of ones
    ones = np.ones(xxr.shape[0]).reshape(xxr.shape[0],1)
    
    # Make Xvals matrix
    Xvals = predict(np.c_[ones, xxr, yyr], w)

    # Plot contour plot
    Xvals = Xvals.reshape(xx.shape)
    ax.contourf(xx, yy, Xvals, cmap=plt.cm.Paired)
    
    # show the plot
    plt.savefig("Perceptron.png")
    plt.show()
    plt.close()

def perceptron_sgd(X, Y,epochs,makeplot):
    w = np.zeros(X.shape[1])
    XX, XX1, YY = read_data('data.txt')
    final_iter = epochs
    
    for epoch in range(epochs):
        print("\n")
        print("epoch: {} {}".format(epoch, '-'*30))
        
        if makeplot:
            plot_boundary(XX,YY,w,epoch)
        
        misclassified = 0
        for i, x in enumerate(X):
            y = Y[i]
            h = np.dot(x, w)*y

            if h <= 0:
                w = w + x*y
                misclassified += 1
                print('misclassified? yes  w: {} '.format(w,i))
                
            else:
                print('misclassified? no  w: {}'.format(w))
                pass

        if misclassified == 0:
            final_iter = epoch
            break
                
    return w, final_iter

def main():
    """Run main function."""

    X, X1, Y = read_data('data.txt')
    max_iter = 20
    w, final_iter = perceptron_sgd(X1,Y,max_iter,False)
    print('w = ', w)
    
    # plot_boundary(X,Y,w,final_iter)
    
    # contour plot
    mesh_stepsize = 0.01
    plot_contour(X,Y,w,mesh_stepsize)

if __name__ == "__main__":
    main()
