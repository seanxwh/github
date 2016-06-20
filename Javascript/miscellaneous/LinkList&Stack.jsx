class Element{
  constructor(value){
    this.value = value;
    this.next = null;
  }
}


class LinkList{
  constructor (llElement){
    if(llElement){
      this.head = llElement;
    }
  }

  append(llElement){
    if(!this.head){
      this.head = llElement;
    }
    else{
      let current = this.head;
      while (current.next){
        current = current.next;
      }
      current.next = llElement;
    }
  }

  remove(value){
    if (this.head.value ==value){
      let next = this.head.next;
      this.head = next;
    }
    else{
      let current = this.head;
      let parent = current;
      while(current.value != value && current.next != null ){
        parent = current ;
        current = current.next;
      }
      if (current.value == value){
        parent.next = current.next;
         console.log(value+ ' has been successfully deleted');
      }
      else {
        console.log(value+ " not found in the list");
      }
    }
 }

 show(){
   let itms=[],
   current = this.head;
   if(this.head){
     while (current.value && current.next){
       itms.push(current.value  );
       current = current.next;
     }
     itms.push(current.value); // push the last itm into the list
   }
   return itms;
 }
}

// subclass of linklist FILO
class stack extends LinkList{
  push(elem){
    super.append(elem);
  }

  pop(){
    let current = this.head,
    parent = current ;
    if (!this.head){
      return null;
    }
    if (!this.head.next){
      let val = this.head.value;
      this.head = null;
      return val;
    }
    while(current.next){
      parent = current;
      current = current.next;
    }
    parent.next = null;
    return current.value || null;
  }
}





console.log("\n" ,"calling Link List ");
// all tests start here
val1 = new Element(1);
val2 = new Element(2);
val3 = new Element(3);
val4 = new Element(1);

LL1 = new LinkList();
// do not append same val, because it will create recusive link
LL1.append(val1);
LL1.append(val2);
LL1.append(val3);
LL1.append(val4);

console.log(LL1.show());

LL1.remove(3);
LL1.remove(3);
console.log(LL1.show());


console.log("\n" ,"calling stack")
val21 = new Element(2);
val31 = new Element(3);
val41 = new Element(1);

stack1 = new stack();
stack1.push(val21);
stack1.push(val31);

console.log(stack1.show());
console.log(stack1.pop());
console.log(stack1.pop());
console.log(stack1.pop());
console.log(stack1.show());
