window.fbAsyncInit = function() {
  FB.init({
    appId: '372111392968616',
    version: 'v2.2',
    cookie: true,
    status: true,
    xfbml: true
  });
};
(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/zh_TW/all.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function processChart(raw) {
  $(function() {
    var COLORS = ["#46BFBD","#43B4DE","#FDB45C","#E4BF33","#949FB1","#4D5360"],
        opt = { responsive:true, scaleShowLabels:false,yAxisFontColor:"#666" },
        ctx = document.getElementById("chartpie").getContext("2d");
    raw.sort(function(a,b){return b.value-a.value});
    var choosen = raw.slice(0, 11);
    var l = [], d = [];
    for (var i = choosen.length - 1; i-- ;) {
      d.push(choosen[i].value);
      l.push(choosen[i].label);
    };
    var data = {
      labels:l,
      datasets: [{
            fillColor: COLORS,
            data:d
      }]
    }
    var bar = new Chart(ctx).HorizontalBar(data, opt),
        total = 0;
    for (var i = raw.length - 1; i--;) {total += raw[i].value;};
    $('#ups').text(total);
    for (var i = 0; i < 10; i++) {
      if(d[i] == 0) break;
      var v = document.createElement('li');
      v.textContent = d[i] + ' / ' + l[i];
      $('#dlist').append(v);
    }
  });
}

function createNode(dt, m, s, p) {
  console.log(m,s,p);
  var d = new Date(dt);
  var itm = document.getElementById("mflow").lastElementChild;
  var optd = { month: "short", day: "2-digit" },
      optt = { hour: "2-digit", minute: "2-digit" },
      cln = itm.cloneNode(true),
      e = cln.firstElementChild;
  e.children[0].children[0].innerHTML = d.toLocaleDateString("en-us", optd);
  e.children[0].children[1].innerHTML = d.toLocaleTimeString("en-us", optt);
  e.children[0].dateTime = d.toLocaleDateString("en-us", $.extend(optd, optt));
  e.children[2].children[0].firstElementChild.innerHTML = m;
  e.children[3].firstElementChild.innerHTML = p + ' | ' + s;
  return cln;
}
$(function() {
  $(".button-collapse").sideNav();
  $(document).pjax('a[data-pjax]', '#main');
});
