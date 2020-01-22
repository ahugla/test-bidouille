#!/usr/bin/env python3
# Your need to tell your OS that this is a Python program, otherwise, it's interpreted as a shell script

"""
send a trace to wavefront using proxy : 

docker run -d \
    -e WAVEFRONT_URL=https://vmware.wavefront.com/api/ \
    -e WAVEFRONT_TOKEN=7xxxxxxxxxxxxxxxxxxxxxxxxxxxx5 \
    -e JAVA_HEAP_USAGE=512m \
    -e WAVEFRONT_PROXY_ARGS="--traceListenerPorts 30000 --histogramDistListenerPorts 40000" \
    -p 2878:2878 \
    -p 30000:30000 \
    -p 40000:40000 \
    wavefronthq/proxy:latest

"""


import time
import opentracing
from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
import wavefront_sdk
import sys
import os
import random
from random import seed
from datetime import datetime



# Calculate time delta
timeBefore=sys.argv[1]
timeAfter=sys.argv[2]
#print('arguments : ' +timeBefore +' et ' +timeAfter)
timeDelta=float(timeAfter) - float(timeBefore)
#time.sleep(timeDelta)   #in sec


# get hostname
myhost = os.uname()[1]
#print('hote  : ' +myhost)



#fichier = open("/var/www/html/script2.log", "a")
#message = 'timeBefore: ' +timeBefore +'  et   timeAfter: ' +timeAfter +'   =>   timeDelta=' +str(timeDelta)
#fichier.write(message)
#fichier.close()



application_tag = wavefront_sdk.common.ApplicationTags(application='TITO',service='journey')
    

# Create Wavefront Span Reporter using Wavefront Proxy Client.
proxy_client = wavefront_sdk.WavefrontProxyClient(
        host='localhost',
        metrics_port=2878,
        distribution_port=40000,
        tracing_port=30000
)

proxy_reporter = WavefrontSpanReporter(client=proxy_client, source=myhost)


# CompositeReporter takes a list of other reporters and invokes them one by one
# Use ConsoleReporter to output span data to console
composite_reporter = CompositeReporter(proxy_reporter, ConsoleReporter())   
#composite_reporter = CompositeReporter(proxy_reporter)   

tracer = WavefrontTracer(reporter=composite_reporter, application_tags=application_tag)



# Create span1, return a newly started and activated Scope.
global_tags = [('Showroom', 'France')]
scope = tracer.start_active_span(
    	operation_name='Google API calls',
        tags=global_tags,
        ignore_active_span=True,
        finish_on_close=True
)
span1 = scope.span


# waiting for timeDelta in order to reproduce the Google API call duration
time.sleep(timeDelta)


# Create span2, child of span1
span2 = tracer.start_span(
    	operation_name='Ingest data',
        references=opentracing.child_of(span1.context),
        tags=global_tags
)
span2.log_kv({'foo': 'bar'})


# Create span2, child of span1
span3 = tracer.start_span(
        operation_name='Analyze',
        child_of=span1,
        tags=global_tags
)


# get random number and sleep for that duration before finishing span2
curr_datetime = datetime.now()
curr_sec = curr_datetime.second
seed(curr_sec)
num=random.random()
time.sleep(num)

span2.finish()




# get random number and sleep for that duration before finishing span3
curr_datetime = datetime.now()
curr_sec = curr_datetime.second
seed(curr_sec)
num=random.random()
time.sleep(num)

span3.finish()


# Create span4 follows from span3.
span4 = tracer.start_span(
        operation_name='Rendering',
        references=opentracing.follows_from(span3.context),
        tags=global_tags
)

curr_datetime = datetime.now()
curr_sec = curr_datetime.second
seed(curr_sec)
num=random.random()
time.sleep(num)

span4.finish()



# Create span5
span5 = tracer.start_span(
        operation_name='Update Database',
        tags=global_tags
)


curr_datetime = datetime.now()
curr_sec = curr_datetime.second
seed(curr_sec)
num=random.random()
time.sleep(num)


span5.finish()


curr_datetime = datetime.now()
curr_sec = curr_datetime.second
seed(curr_sec)
num=random.random()
time.sleep(num)


# Close the scope
scope.close()

# Close the tracer
tracer.close()
    

