// a simple pub/sub implementation

class pubSubEventEmitter {
  constructor(ch){
    this.ch = ch;
    this.fns = {};
  }
  subscribe(name, fn){
    this.fns[name]=fn;
    return this;
  }
  unsubscribe(name){
    delete this.fns[name];
    return null;
  }
  publish(data){
   for (var key in this.fns){
     this.fns[key](data);
   }
   return this;
  }

}


const channel = new pubSubEventEmitter('ch1');
channel.subscribe('c1',(data)=>console.log(data+ ' from channel_1'));
channel.subscribe('c1_1',(data)=>console.log(data+ ' from channel_1 again'));

setTimeout(()=>{
  channel.publish('something');
  channel.unsubscribe('c1');
},2000);

setTimeout(()=>{
  channel.publish('something else');
},4000);
