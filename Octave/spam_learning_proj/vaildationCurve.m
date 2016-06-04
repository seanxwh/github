function[C_vec,model,err_tr,err_va,err_ts] =vaildationCurve(X_TR,Y_TR,X_VA,Y_VA,X_TS,Y_TS)
    C_vec = [0 0.001 0.003 0.01 0.03 0.1 0.3 1 3 10]';
    model = [];
    for i=1:length(C_vec)
     model = svmTrain(X_TR,Y_TR,C_vec(i),@linearKernel);
     p1=svmPredict(model,X_TR);
     p2=svmPredict(model,X_VA);
     p3=svmPredict(model,X_TS);
     err_tr(i) = mean(double( p1== Y_TR)) * 100;
     err_va(i) = mean(double( p2== Y_VA)) * 100;
     err_ts(i) = mean(double( p3== Y_TS)) * 100;
    end
end