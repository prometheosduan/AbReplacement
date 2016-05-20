# AbReplacement<br />
a wheel inspired by tarekziade/boom<br />
<br />
Installation:<br />
pip install gevent<br />
pip install requests<br />
or simply:<br />
pip install boom<br />
<br />
Quickstart:<br />
$ python test.py -n 100 -c 25 -m POST 'https://www.google.com'<br />

Namespace(concurrency=25, method='POST', requests=100, url='https://www.google.com')<br />
Starting the load [====================================================================================================] Done<br />
<br />
Successful calls                100<br />
Total time                      3.6906 s<br />
Average                         0.7612<br />
Fastest                         0.3792<br />
Slowest                         1.8654<br />
