const concatString = (prevString,strings)=>prevString.concat(strings);

const checkDivisible = (num, divisor) => (num%divisor==0);

// the reducer function that call the checking function(checkFn) with current iterating number and divisor (currentKey) from the conditions. If the checking function satisfy, then call the modification function
const reduceFn = (previousContent, currentKey, obj, number, checkFn = checkDivisible ,modFn = concatString)=>{
  let keyToNum = Number(currentKey);
  let currentContent = previousContent;
  if(checkFn(number,keyToNum)){
    currentContent = modFn(currentContent, obj[keyToNum]);
  }
  return currentContent;
};

const checkAndReturn = (number, conditions={},reducerFn=reduceFn)=>{
  let returnContent = number;
  const conditionkeys = Object.keys(conditions);
  if (conditionkeys.length>0){
      let newContent = conditionkeys.reduce((previousContent,currentKey) => {
        return reducerFn(previousContent, currentKey,conditions, number);
    },'');
   if(newContent != ''){
     returnContent = newContent;
   }
  }
  return returnContent;
};


const conditions={
  3: 'Fizz',
  5: 'Buzz'
}; //can add in additional conditions

for (i=1; i<=100; i++){
  console.log(checkAndReturn(i, conditions));
}
