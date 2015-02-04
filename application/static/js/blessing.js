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
    var COLORS = [{f:"#F7464A", b:"#FF5A5E"},
                  {f:"#46BFBD", b:"#5AD3D1"},
                  {f:"#43B4DE", b:"#57C8F2"},
                  {f:"#FDB45C", b:"#FFC870"},
                  {f:"#E4BF33", b:"#F8D347"},
                  {f:"#949FB1", b:"#A8B3C5"},
                  {f:"#4D5360", b:"#616774"}];
    var ctx = document.getElementById("chartpie").getContext("2d");

    function getColored(raw) {
      for (var i = raw.length - 1; i >= 0; i--) {
        raw[i].color = COLORS[i % COLORS.length].f;
        raw[i].highlight = COLORS[i % COLORS.length].b;
      };
      return raw;
    }

    raw.sort(function(a,b){return b.value-a.value});
    var data = getColored(raw.slice(0, 11)),
        doughnut = new Chart(ctx).Doughnut(data),
        total = 0;
    for (var i = raw.length - 1; i--;) {
      total += raw[i].value;
    };
    $('#ups').text(total);
    for (var i = 0; i < 10; i++) {
      if(data[i].value == 0) break;
      var v = document.createElement('li');
      v.textContent = data[i].label + ' / ' + data[i].value;
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
  $('.go').click(function(event){
    $('ul.tabs').tabs('select_tab', 'blessing');
    $(document).scrollTop( $("#header").offset().top );
    e.preventDefault();
  });
  $('.scrollspy').scrollSpy();
  $('.tooltipped').tooltip({delay: 50});
  $('select').material_select();

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
});
