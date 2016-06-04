clc,clear;
load('hamHard.mat');    %disable the following 3 lines if undisable line 5-7(save comuptation if using provided 4000 words dictionary) 
load('hamEasy.mat');
load('spam.mat');
%spamVocabMatrix=filesToVocabMatrix('learning_sets/spam_2');
%hamEasyVocabMatrix=filesToVocabMatrix('learning_sets/easy_ham_2');
%hamHardVocabMatrix=filesToVocabMatrix('learning_sets/hard_ham');

%construct corresponding output for different type of email
Yspam=ones(size(spamVocabMatrix,1),1);
YhamEasy=zeros(size(hamEasyVocabMatrix,1),1);
YhamHard=zeros(size(hamHardVocabMatrix,1),1);

X_tot=[spamVocabMatrix;hamEasyVocabMatrix;hamHardVocabMatrix];
Y_tot=[Yspam;YhamEasy;YhamHard];

%randomize the input test set after cascade,and keep the output
%corresponding to the right input after randomization
idx=randperm(size(X_tot,1));
X_tot=X_tot(idx,:);
Y_tot=Y_tot(idx,:);

%seperate into 3 type of catagories
[X_TR,X_VA,X_TS]=dataSeperation(X_tot);
[Y_TR,Y_VA,Y_TS]=dataSeperation(Y_tot);

%train model and vailidate model in train,cross-vailidation,test these
%three catagories
[C_vec,model,err_tr,err_va,err_ts]=vaildationCurve(X_TR,Y_TR,X_VA,Y_VA,X_TS,Y_TS);
plot(C_vec,err_tr,'g',C_vec,err_va,'b--o',C_vec,err_ts,'r');
ylim([90,100]);
title('2-D C VS Accuracy Plot');
xlabel('C Value');
ylabel('Accuacy (%)');
legend('y = Train Accuracy','y = Validation Accuracy','y = Test Accuracy');

