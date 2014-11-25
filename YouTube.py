from urllib import urlopen, unquote, urlencode; 
from urlparse import urlparse, parse_qs; 
import re
import execjs, wget

pattern = r'(http.*?);'

url="http://www.youtube.com/watch?v=XXH0iMX0m3o"
video_id = urlparse(url).query.split('=')[-1]
url_info = 'http://www.youtube.com/get_video_info?video_id={}'.format(video_id)
#print urlopen(url_info).read()
print parse_qs(urlopen(url_info).read())['use_cipher_signature']
#informacje o video, ktore mozemy uzyskac
a=unquote(parse_qs(
    urlopen(url_info).read())['url_encoded_fmt_stream_map'][0]).decode('utf-8')
linki=re.findall(pattern, a)


print linki[0]
p=urlparse(linki[0])
print p.scheme
print p.netloc
print p.path

#zastapienie znakow "," znakami "&"
for x in linki:
    x.replace(',', '&')
    print x

tab=[]
# rozlozenie linka na czesci
for x in linki:
    tab.append(parse_qs(urlparse(x).query))

for i, x in enumerate(tab):
    print x.keys()
    try:
        print x['type'], x['quality']
    except:
        print 'nie ma'
    print i
    
#print urlencode(tab[0])

ctx = execjs.compile("""
var wq={aJ:function(a){a.reverse()},KO:function(a,b){a.splice(0,b)},Gs:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b]=c}};function xq(a){a=a.split("");wq.KO(a,2);wq.aJ(a,52);wq.KO(a,3);wq.aJ(a,7);wq.KO(a,3);wq.aJ(a,4);wq.Gs(a,2);return a.join("")}
""")
print tab[0]['signature']
tab[0]['signature']=unicode(ctx.call('xq', str(tab[0]['signature'])))
print tab[0]['signature']
link = p.scheme+'://'+p.netloc+p.path+'?'+urlencode(tab[0])

print link
#open(video_id+'.mp4', 'wb').write(urlopen(link).read())
filename, ext = wget.download(link)
print filename
