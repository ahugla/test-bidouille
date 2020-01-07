

import time
import wavefront_sdk
#import wavefront_sdk.common
import wavefront_opentracing_sdk
#import wavefront_opentracing_sdk.reporting



# Set Up Application Tags
# -----------------------
# metadata (span tags) that are included with every span reported to Wavefront
# https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python

from wavefront_sdk.common import ApplicationTags
application_tags = ApplicationTags(application="ALEXapp", service="ALEXsvc")
# application : apparait dans la vue 'application status'
# service     : 




# Set Up a Wavefront Sender
# -------------------------
# A "Wavefront sender" is an object that implements the low-level interface for sending data to Wavefront.

from wavefront_sdk import WavefrontProxyClient

# Create a sender with:
   # the proxy hostname or address
   # the recommended listener port (30000) for sending trace data to 
   # the recommended listener port (2878) for sending histograms to 
   # the default listener port (2878) for sending metrics to 
   # a nondefault interval (2 seconds) for flushing data from the sender to the proxy. Default: 5 seconds
wavefront_sender = WavefrontProxyClient(
   host="localhost",      # MARCHE AVEC LOCALHOST!!!!!
   tracing_port=30000,
   distribution_port=2878,
   metrics_port=2878
   #internal_flush=2
)




# Set Up a Reporter
#--------------------
# to report trace data to Wavefront


from wavefront_sdk import WavefrontProxyClient


wf_span_reporter = wavefront_opentracing_sdk.reporting.WavefrontSpanReporter(
    client=wavefront_sender,
    source='ALEXH_tracing-example'   # optional nondefault source name - Apparait comme filtre dans "Application status / Details"
)


# To get failures observed while reporting.
total_failures = wf_span_reporter.get_failure_count()





# Create the WavefrontTracer
#-----------------------------
# To create a WavefrontTracer, you pass the ApplicationTags and Reporter instances you created in the previous steps:

from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter

# Construct Wavefront opentracing Tracer
tracer = wavefront_opentracing_sdk.WavefrontTracer(
    reporter=wf_span_reporter,
    application_tags=application_tags)



# Create span1, return a newly started and activated Scope.
scope = tracer.start_active_span(
    operation_name='span1',
    tags=[('alexkey1','alexvalue1')],
    ignore_active_span=True,
    finish_on_close=True
)
span1 = scope.span
time.sleep(1)



span3 = tracer.start_span(
        operation_name='span3',
        child_of=span1,
        tags=[('alexkey2','alexvalue2')]
    )
time.sleep(1)

span3.finish()



# "Tracer.start_span()" and "Tracer.start_active_span()" will automatically use the current active Span as a parent, 
# unless the programmer passes a specified parent context or sets "ignore_active_span=True"






#  ON NE CLOSE PAS SPAN1 ???   en fait c'est fermé avec Scope.close?


# Close the scope
scope.close()




# exit
#Always close the tracer before exiting your application to flush all buffered spans to Wavefront.

tracer.close()