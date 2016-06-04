const split=(arr)=>{
  if(!Array.isArray(arr) || arr.length == 0){
    throw "not an array";
  }
  else{
    let lst = [];
    const length = arr.length;
// split array into two arrays if the input array size is bigger than one, otherwise return input array
    if(length>1){
      itm1 = arr.slice(0,Math.floor(length/2));
      lst.push(itm1);
      itm2 = arr.slice(Math.floor(length/2),length);
      lst.push(itm2);
    }
    if(length == 1){
      lst = arr;
    }
    return lst;
  }
};

// console.log(split([2,4]));


// merge two sorted lists
const merge=(arr1, arr2)=>{
  if(!Array.isArray(arr1)||arr1.length==0||!Array.isArray(arr2)||arr2.length==0){
    throw "not an array";
  }
  else{
    let newArray=[],
        i=0,
        j=0;
    while(i<arr1.length && j<arr2.length){
      if(arr1[i]<arr2[j] && i<arr1.length){
        newArray.push(arr1[i]);
        i++;
      }
      else if(arr1[i] > arr2[j] && j<arr2.length){
        newArray.push(arr2[j]);
        j++;
      }
      else if(arr1[i] == arr2[j]){
        newArray.push(arr2[j]);
        j++;
        newArray.push(arr1[i]);
        i++;
      }
    }
    remainArray = arr1.slice(i).concat(arr2.slice(j));//merge the remaining of any of the two sorted lists
    newArray = newArray.concat(remainArray);
    return newArray;
  }
};

// console.log(merge([1],[0,5,7]));

const mergeSort=(arr)=>{
  if(!Array.isArray(arr) || arr.length == 0){
    throw "not an array";
  }
  else if (arr.length == 1){
    return arr;
  }
  else{
    let mergelst = [],
    newArray = [],
    lst = split(arr);
    for (var i = 0; i<lst.length; i++){
      if (lst[i].length == 1){
        mergelst[i] = lst[i];// if the list contains only single item, use that for the input of merge
      }
      else{
        mergelst[i] = mergeSort(lst[i]);
      }
    }
    newArray = merge(mergelst[0],mergelst[1]);//this is assuming the merge only split into two parts
    return newArray;
  }
};

console.log(mergeSort([1]));//[1]
console.log(mergeSort([3,2]));//[2, 3]
console.log(mergeSort([0,5,4,3,6,7,3,6,9,-14,100]));//[-14, 0, 3, 3, 4, 5, 6, 6, 7, 9, 100]
console.log(mergeSort([]));//Uncaught not an array
