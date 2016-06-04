clc,clear;
%load('hamHard.mat');    %disable the following 3 lines if undisable line 5-7(save comuptation if using provided 4000 words dictionary) 
%load('hamEasy.mat');
%load('spam.mat');
spamVocabMatrix=filesToVocabMatrix('learning_sets/spam_2');
userSpamVocabMatrix=filesToVocabMatrix('learning_sets/user_spam');
hamEasyVocabMatrix=filesToVocabMatrix('learning_sets/easy_ham_2');
hamHardVocabMatrix=filesToVocabMatrix('learning_sets/hard_ham');
userHamVocabMatrix=filesToVocabMatrix('learning_sets/user_ham');


%construct corresponding output for different type of email
Yspam=ones(size(spamVocabMatrix,1),1);
YuserSpam=ones(size(userSpamVocabMatrix,1),1);
YhamEasy=zeros(size(hamEasyVocabMatrix,1),1);
YhamHard=zeros(size(hamHardVocabMatrix,1),1);
YuserHam= zeros(size(hamHardVocabMatrix,1),1);

X_tot=[spamVocabMatrix;userSpamVocabMatrix;hamEasyVocabMatrix;hamHardVocabMatrix;userHamVocabMatrix];
Y_tot=[Yspam;YuserSpam;YhamEasy;YhamHard;YuserHam];

%X_tot=[spamVocabMatrix;hamEasyVocabMatrix;hamHardVocabMatrix];
%Y_tot=[Yspam;YhamEasy;YhamHard;];

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


%use classify user's input emails by asking use to input a personal email
%also asve user's email and make them for future traininig 
P = questdlg ('use your email ?','train spam classifier yourself');
toggle = 0 
if(P =="Yes")
  toggle = 1;
endif
do
  isSpam = 0;
  output = 'ham';
  dialog=inputdlg('Email Content', 'Check an email'){1}
  id = mat2str(mktime (localtime (time ())))
  save (id, dialog)
  file_contents = readFile(id)
  word_indices  = processEmail(dialog3)
  emailfeatures4 = emailFeatures(wi4)'
  %silent_functions(1);
  isSpam=svmPredict(model,emailfeatures);
  if(isSpam)
    output = 'spam'
  endif
  a = questdlg(strcat('this email is ',output),'predicted email type');
  if (a=='No')%correct the precdiction 
    isSpam = !isSpam;
  endif
  if(isSpam)
    movefile(id,'../learning_sets/user_spam');
  else 
    movefile(id,'../learning_sets/user_spam');
  endif
  P = questdlg ('use your email again?','train spam classifier yourself');
  if(P =="Yes")
    toggle=1;
  else
    toggle=0;
  endif
until(toggle == 0)