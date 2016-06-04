function[filesToEmailVocabMatrix]=filesToVocabMatrix(pwd)
    filesMatrix=getAllFiles(pwd);
    filesToEmailVocabMatrix=emailVocabMatrix(filesMatrix);
end