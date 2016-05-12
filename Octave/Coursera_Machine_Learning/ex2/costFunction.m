function [J,grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

%   X : M(trail) by N((features) matrix( N feature elements in X, in M trails),
%   theta(coeffiecient of each feature elements N by 1)  
%   Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%
h_theta=1./(1+exp(-X*theta)); %likelyhood of the output by ML (M by 1)
J = 1/m*(-(y'*log(h_theta))-((1-y)'*log(1-h_theta)));
delta=((h_theta-y));
grad =(1/m)*(X'*delta);



% =============================================================