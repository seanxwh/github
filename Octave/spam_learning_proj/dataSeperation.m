function [input_tr,input_va,input_ts]= dataSeperation(input_matrix)
  [m,n]=size(input_matrix);
  input_tr = input_matrix(1:ceil(.6*m),:);
  input_va = input_matrix(ceil(.6*m)+1:ceil(.8*m),:);
  input_ts = input_matrix(ceil(.8*m)+1:m,:);
%  silent_functions(1);
end
