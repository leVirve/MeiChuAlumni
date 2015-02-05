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
    var choosen = raw.slice(0, 11);
    var COLORS = ["#46BFBD","#43B4DE","#FDB45C","#E4BF33","#949FB1","#4D5360","#46BFBD","#43B4DE","#FDB45C","#E4BF33","#949FB1","#4D5360"],
        l = [], d = [];
    for (var i = choosen.length - 1; i >= 0 ;i--) {
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
    var opt = { responsive:true,
          graphTitle: "前十大留言系級",
          scaleShowLabels:false,
          scaleOverride : true,
          scaleStartValue : 0,
          scaleSteps : 5,
          scaleStepWidth : Math.max.apply(null, d) / 5,
        },
        // opt = { responsive:true, scaleShowLabels:false },
        ctx = document.getElementById("chartpie").getContext("2d");
    raw.sort(function(a,b){return b.value-a.value});
    var bar = new Chart(ctx).HorizontalBar(data, opt), total = 0;
    for (var i = raw.length - 1; i >= 0; i--) {total += raw[i].value;};
    $('#ups').text(total);
  });
}

$(function() {
  $(".button-collapse").sideNav();
  $(document).pjax('a[data-pjax]', '#main');
});
