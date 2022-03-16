import numpy as np

def cost_function(x, y, w, b):
    cost = np.sum((((x.dot(w) + b) - y) ** 2) / (2 * len(y))) # squared error (predicted value - actual value) ^ 2
    return cost

def gradient_descent(x, y, w, b, learning_rate, epochs):
    cost_list = [0] * epochs
    epoch_arr = []

    for epoch in range(epochs):
        z = x.dot(w) + b
        loss = z - y # predicted value - actual value
        
        weight_gradient = x.T.dot(loss) / len(y) # descent
        bias_gradient = np.sum(loss) / len(y) # offset
        
        w = w - learning_rate * weight_gradient # main update
        b = b - learning_rate * bias_gradient
  
        cost = cost_function(x, y, w, b) # cost function is a single number counted in each iteration
        cost_list[epoch] = cost
        
        epoch_arr.append(epoch)
        
        if (epoch % (epochs / 10) == 0):
            #print("Cost at epoch", epoch, "is:", cost)
            print("EPOCH: ", epoch)
        
    return w, b, cost_list, epoch_arr

def predict(X, w, b):
    return X.dot(w) + b # final form (takes w and b matrices from gradient function)
