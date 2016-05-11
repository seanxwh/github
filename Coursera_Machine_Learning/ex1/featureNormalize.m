function [X_norm, mu, sigma] = featureNormalize(X)
%FEATURENORMALIZE Normalizes the features in X 
%   FEATURENORMALIZE(X) returns a normalized version of X where
%   the mean value of each feature is 0 and the standard deviation
%   is 1. This is often a good preprocessing step to do when
%   working with learning algorithms.
%   M (examples) by N (features) 
% You need to set these values correctly

% ====================== YOUR CODE HERE ======================
% Instructions: First, for each feature dimension, compute the mean
%               of the feature and subtract it from the dataset,
%               storing the mean value in mu. Next, compute the 
%               standard deviation of each feature and divide
%               each feature by it's standard deviation, storing
%               the standard deviation in sigma. 
%
%               Note that X is a matrix where each column is a 
%               feature and each row is an example. You need 
%               to perform the normalization separately for 
%               each feature. 
%
% Hint: You might find the 'mean' and 'std' functions useful.
%       




length=size(X,1); % length of M 
mu = mean(X);	% 1 by N matrix
mu_matrix=ones(length,1)*mu; %create a M by 1  1’s matrix, and multiple it by 1 by N matrix, to result a M by N matrix
sigma = std(X);
sigma_matrix=ones(length,1)*sigma; %create M by N std matrix
X_norm = (X-mu_matrix)./sigma_matrix;




% ============================================================

end
