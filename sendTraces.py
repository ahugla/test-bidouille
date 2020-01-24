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

"""

Utilization de "sendTraces.py":
sendTraces.py [time_before] [time_after] [Home_Address] [Work_Address]

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



# function to get a random number < 1
def getRandomNumber():
    curr_datetime = datetime.now()
    curr_sec = curr_datetime.second
    seed(curr_sec)
    num=random.random()
    return num



# Calculate time delta
timeBefore=sys.argv[1]
timeAfter=sys.argv[2]
#print('arguments : ' +timeBefore +' et ' +timeAfter)
timeDelta=float(timeAfter) - float(timeBefore)


# get Addresses
Home_Address=sys.argv[3]
Work_Address=sys.argv[4]


# get hostname
myhost = os.uname()[1]
#print('hote  : ' +myhost)


# get wavefront PROXY_NAME and PROXY_PORT  
proxy_name=os.getenv('PROXY_NAME')    # retourne None si n'existe pas
proxy_port=os.getenv('PROXY_PORT')    # retourne None si n'existe pas
print(proxy_name)
print(proxy_port)




if proxy_name != 'None' and proxy_port != 'None':

  print('AUCUN EST A None')
  
  application_tag = wavefront_sdk.common.ApplicationTags(application='TITO',service='journey')
    

  # Create Wavefront Span Reporter using Wavefront Proxy Client.
  proxy_client = wavefront_sdk.WavefrontProxyClient(
          host=proxy_name,
          metrics_port=proxy_port,
          distribution_port=40000,
          tracing_port=30000
  )

  
  proxy_reporter = WavefrontSpanReporter(client=proxy_client, source=myhost)


  # CompositeReporter takes a list of other reporters and invokes them one by one
  # Use ConsoleReporter to output span data to console
  #composite_reporter = CompositeReporter(proxy_reporter, ConsoleReporter())   
  composite_reporter = CompositeReporter(ConsoleReporter())   
  #composite_reporter = CompositeReporter(proxy_reporter)   


  tracer = WavefrontTracer(reporter=composite_reporter, application_tags=application_tag)



  # Create span1, return a newly started and activated Scope.
  global_tags = [('Showroom', 'France')]
  scope = tracer.start_active_span(
      	operation_name='journeyRequest',
          tags=global_tags,
          ignore_active_span=True,
          finish_on_close=True
  )
  span1 = scope.span



  # Create span2, child of span1
  span2 = tracer.start_span(
      	operation_name='ParseRequest',
          references=opentracing.child_of(span1.context),
          tags=global_tags
  )


  # waiting for timeDelta in order to reproduce the Google API call duration
  time.sleep(getRandomNumber())
  span2.finish()


  # Create span3
  dedicated_tags = [('Showroom','France'),('Home_Address',Home_Address),('Work_Address',Work_Address)]
  span3 = tracer.start_span(
          operation_name='Google API calls',
          #child_of=span1,
          tags=dedicated_tags
  )


  time.sleep(timeDelta)  # en sec, accepte des floats
  span3.finish()


  # Create span4
  span4 = tracer.start_span(
          operation_name='DBupdate',
          #child_of=span1,
          tags=global_tags
  )


  time.sleep(getRandomNumber())
  span4.finish()



  # Create span5
  span5 = tracer.start_span(
          operation_name='Rendering',
          #child_of=span1,
          tags=global_tags
  )


  time.sleep(getRandomNumber())
  span5.finish()


  scope.close()


  # Close the tracer
  tracer.close()
      

else:
  print('Au moins une variable d environnement wavefront n existe pas')


