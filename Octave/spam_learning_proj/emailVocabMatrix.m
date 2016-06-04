function[x]=emailVocabMatrix(matrix_set)
word_indices=[];
x=[];
  for(i=1:length(matrix_set))
    file_contents = readFile(matrix_set{(i)});
    word_indices  = processEmail(file_contents);
    x = [x, emailFeatures(word_indices)];
  end
x=x';
%silent_functions(1);
end
