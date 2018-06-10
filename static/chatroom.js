var socket = io.connect('http://' + document.domain + ':' + location.port);
var self = "#";
window.onload = function() {
  var width = $('#umsg').width();
  $('#chat').width(width+'px');
}
socket.on("connect", function() {
  socket.emit("joined");
});

socket.on("connected", function(data) {
  var dataObj = JSON.parse(data);
  if(self == "#") self = dataObj.sender;
});

socket.on("status", function(data) {
  var dataObj = JSON.parse(data);
  var name = dataObj.sender;
  var msg = dataObj.msg;
  name = '<b>'+name+'</b>';
  $('#chat').html($('#chat').html() + "<div class='row'><"+name+msg+"></div>");
  $('#chat').scrollTop($('#chat')[0].scrollHeight);
});

socket.on("incoming", function(data) {
  var dataObj = JSON.parse(data);
  var name = dataObj.sender;
  var msg = dataObj.msg;
  name = '<b>'+name+'</b>: ';
  $('#chat').html($('#chat').html()+"<div class='row'>"+name+msg+"</div>");
  $('#chat').scrollTop($('#chat')[0].scrollHeight);
});

socket.on("close", function(data) {
  var dataObj = JSON.parse(data);
  var name = dataObj.sender;
  var url = dataObj.url;
  console.log("self= "+self+" name="+name);
  if(self == name)
  {
    socket.disconnect();
    window.location.href = url;
  }
});

function sendmsg()
{
  var msg = $('#umsg').val();
  $('#umsg').val('');
  socket.emit("outgoing", {"msg": msg});
}

function leave_room()
{
  socket.emit("exit");
}
