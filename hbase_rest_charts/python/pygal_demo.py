#!/usr/bin/env python 
# -*- coding: UTF-8 -*-

'''
- Following:
  * https://gist.github.com/rduplain/1641344 <-- Flask + Matplotlib
  * http://en.m.wikipedia.org/wiki/Matplotlib <-- more Matplotlib

- Dependencies:
$ sudo yum install libpng-devel.x86_64
$ sudo pip2.7 install flask matplotlib requests

for pygal install lxml
        - Site: http://lxml.de/tutorial.html
        - Installation:

(py27env)[cloudera@localhost bicing-bcn]$ sudo yum install python-lxml.x86_64
<-- that installs it for python2.6 omming with the system

For python 2.7 installed from sources in CentOS 6 (http://stackoverflow.com/questions/5178416/pip-install-lxml-error), we first need to manually install some dependencies:

(py27env)[cloudera@localhost bicing-bcn]$ sudo yum install libxslt-python.x86_64 libxslt-devel.x86_64 libxslt-devel.i686 libxml2-devel.x86_64 libxml2-devel.i686 libxml2-python.x86_64

    (py27env)[cloudera@localhost bicing-bcn]$ sudo pip2.7 install lxml

and then 

$ sudo pip2.7 install pygal

- Start HBase REST server:

$ hbase rest start -ro -p 9998

$  curl -H "Accept: application/json" http://localhost:9998/test_hbase_py_client/john
{"Row":[{"key":"am9obg==","Cell":[{"column":"aW5mbzphZ2U=","timestamp":1393791170961,"$":"NDI="},{"column":"dmlzaXRzOmFtYXpvbi5jb20=","timestamp":1393791171026,"$":"NQ=="},{"column":"dmlzaXRzOmdvb2dsZS5lcw==","timestamp":1393791171063,"$":"Mg=="}]}]}(py27env)[cloudera@localhost hbase_rest_charts]$ 

hbase(main):002:0> scan 'test_hbase_py_client'
ROW                                              COLUMN+CELL                                                                                                                                
 john                                            column=info:age, timestamp=1393791170961, value=42                                                                                         
 john                                            column=visits:amazon.com, timestamp=1393791171026, value=5                                                                                 
 john                                            column=visits:google.es, timestamp=1393791171063, value=2                                                                                  
 mary                                            column=info:age, timestamp=1393791170995, value=26                                                                                         
 mary                                            column=visits:amazon.com, timestamp=1393791171079, value=4                                                                                 
 mary                                            column=visits:facebook.com, timestamp=1393791171098, value=2   
'''
from flask import Flask, make_response
from flask import render_template

# For matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO

import pygal
from pygal.style import DarkSolarizedStyle

import requests
from collections import deque

_hbase_base_url='http://localhost:9998/'
values = [1,0,2, 5, 7, 2]

app = Flask(__name__)
if not hasattr(app, 'extensions'):
    app.extensions = {}
app.extensions['values'] = deque(values)

@app.route('/barchart.png')
def plotOne():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(range(len(values)), values)

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/barchart.svg')
def graph_something():
     bar_chart = pygal.Bar(style=DarkSolarizedStyle)
     # bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
     bar_chart.add('Values', app.extensions['values'])
     app.extensions['values'].rotate(1)
     return bar_chart.render_response()

@app.route('/barchart.html')
def barchart(refresh_rate=5):
    ''' 
    By default jinja2 will look for templates at the templates folder 
    in the root of the application.
    By using the template be get autorefresh by using a <meta> header
    '''
    return render_template('barchart.html', refresh_rate=refresh_rate)

if __name__ == '__main__':
    import sys
    print 'Usage: <port>'
    port = int(sys.argv[1])
    print 'Go to http://127.0.0.1:{port}/barchart.html, http://127.0.0.1:{port}/barchart.png, http://127.0.0.1:{port}/barchart.svg'.format(port=port)

    app.run(debug=True, port=port)