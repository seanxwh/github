#Spam Ham Classifier
this is a project built motivated by Coursera Machine Learning HW6 and utilize partial of its code

#What does the classifier do 

- this is a spam or ham classifier that built by using the the spam/ham data set from </br>
https://spamassassin.apache.org/publiccorpus/ </br>
a copy of data is downloaded under the 'learning_set/' directory </br>
  
- the classifier will fisrt build a dictionary using the common daily words from </br>
http://www.wordfrequency.info</br>
the list of common daily words for the classifier is '4000_words.txt' in directory 

- stamp each of the dataset(spam or ham) with the dictionary(i.e create a dictionary vector for each training set)</br>

- run linear kennel SVM on the training, validation, and test set of the data, we can get a ~97% accuracy in test set</br>

- one can also input email content into the classifier, and let the classifier predict the type </br>

- the classifier will store the user input data for future training</br>


To run the program in matlab/octave, excute 'excution' under the current directory

