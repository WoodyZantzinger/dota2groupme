# remindme task do-er

import urllib2

response = urllib2.urlopen('http://young-fortress-3393.herokuapp.com/remindme')
html = response.read()
print(html)

