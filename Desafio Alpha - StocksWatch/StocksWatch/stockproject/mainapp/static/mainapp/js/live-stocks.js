const roomName = JSON.parse(document.getElementById('room-name').textContent)
var queryString = window.location.search;
queryString = queryString.substring(1);
console.log(queryString);
const stockSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/stock/' + roomName + '/' + '?' + queryString
);

stockSocket.onmessage = function(e) {
  console.log(e.data);
  const data = JSON.parse(e.data);
  console.log(data);
  for (const [key, value] of Object.entries(data)){
    var price = Number((value['Quote Price']).toFixed(4));
    var prevprice = Number((value['Previous Close']).toFixed(4));
    document.getElementById(key + '_price').innerHTML = price;
    document.getElementById(key + '_prevprice').innerHTML = prevprice;
    document.getElementById(key + '_open').innerHTML = value['Open'];
    document.getElementById(key + '_range').innerHTML = value['52 Week Range'];
    document.getElementById(key + '_cap').innerHTML = value['Market Cap'];
    document.getElementById(key + '_volume').innerHTML = value['Volume'];
    var change = document.getElementById(key + '_price').innerHTML - document.getElementById(key + '_prevprice').innerHTML;
    change = Number((change).toFixed(4));
    if (change >= 0){
      document.getElementById(key + '_change').className = "green";
      document.getElementById(key + '_change').innerHTML = change;
    }
    else if (change < 0){
      document.getElementById(key + '_change').className = "red";
      document.getElementById(key + '_change').innerHTML = change;
    }
  }
}