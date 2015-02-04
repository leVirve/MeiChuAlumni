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
    var COLORS = [
                 "#46BFBD",
                 "#43B4DE",
                 "#FDB45C",
                 "#E4BF33",
                 "#949FB1",
                 "#4D5360"];
var opt = {
responsive:true
}
    var ctx = document.getElementById("chartpie").getContext("2d");

    raw.sort(function(a,b){return b.value-a.value});
    var choosen = raw.slice(0, 11);
    var l = [], d = [];
    for (var i = choosen.length - 1; i-- ;) {
      d.push(choosen[i].value);
      l.push(choosen[i].label);
    };
    var data = {
      labels:l,
      datasets: [
        {
            label: "My First dataset",
            fillColor: COLORS,
            // strokeColor: "rgba(220,220,220,0.8)",
            data: d
        }
      ]
    }
    var bar = new Chart(ctx).HorizontalBar(data, opt),
        total = 0;
    for (var i = raw.length - 1; i--;) {
      total += raw[i].value;
    };
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
  var d = new Date(dt);
  var itm = document.getElementById("mflow").lastElementChild;
  var optd = { month: "short", day: "2-digit" },
      optt = { hour: "2-digit", minute: "2-digit" },
      cln = itm.cloneNode(true),
      e = cln.firstElementChild;
  e.children[0].children[0].textContent = d.toLocaleDateString("en-us", optd);
  e.children[0].children[1].textContent = d.toLocaleTimeString("en-us", optt);
  e.children[0].dateTime = d.toLocaleDateString("en-us", $.extend(optd, optt));
  e.children[2].children[0].textContent = m;
  e.children[3].children[0].textContent = p + ' | ' + s;
  return cln;
}

$(function() {
  $('#content').click(function(){$("#wrap").load("../static/content.html");return false;})
  // $('#blessings').click(function(){$("#wrap").load("form.html");return false;})
  // $('.go').click(function(event){
  //   $('ul.tabs').tabs('select_tab', 'blessing');
  //   $(document).scrollTop( $("#header").offset().top );
  //   e.preventDefault();
  // });
  $('.tooltipped').tooltip({delay: 50});
  $('select').material_select();
  $('.slider').slider({full_width: true});
  $('[href="#photo"]').click(function() {
    setTimeout(function() {
      location.href = '/photo';
    }, 1000);
  });

  $('#new-message-form').submit(function(){
    $.post($(this).attr('action'), $(this).serialize(), function(d) {
      toast('資料送出!', 4000);
      var b = document.createElement('button');
      b.innerHTML = '分享';
      b.className = 'btn waves-effect waves-light right';
      b.onclick = function() {
        FB.ui({
          method: 'feed',
          link: window.location.href,
        },
        function(response) {
          if (response && response.post_id) {
            toast('分享成功!', 4000);
            $.post("/blessings/update", {'c':response.post_id,'d':d.mid},
              function(){}
            );
          }
          location.reload();
        });
      }
      var c = createNode(new Date(), $('textarea[name="description"]').val(), $('#grade').val(), $('select[name="department"] option:selected').val());
      p = document.getElementById("mflow");
      p.insertBefore(c, p.firstChild);
      $('#somewhere').append(b);
      $('#new-message-form')[0].remove();
    }, 'json');
    return false;
  });
  for (var i = 60; i <= 99; i++) {
    $('select[name="grade"]').append(new Option(i, i));
  };
  for (var i = 00; i <= 18; i++) {
    $('select[name="grade"]').append(new Option(i, i));
  };
});
