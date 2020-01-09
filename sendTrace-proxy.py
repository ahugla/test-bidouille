"""
send a trace to wavefront using proxy

docker run -d \
    -e WAVEFRONT_URL=https://vmware.wavefront.com/api/ \
    -e WAVEFRONT_TOKEN=73e0e166-5b8b-4877-9ad8-102d3374ee45 \
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


application_tag = wavefront_sdk.common.ApplicationTags(application='ALEXapp',service='ALEXsvc')
    

# Create Wavefront Span Reporter using Wavefront Proxy Client.

proxy_client = wavefront_sdk.WavefrontProxyClient(
        host='localhost',
        metrics_port=2878,
        distribution_port=40000,
        tracing_port=30000
        # internal_flush=2  not working 
)
proxy_reporter = WavefrontSpanReporter(client=proxy_client, source='ALEXH_tracing-example')


# Create Composite reporter.
# Create Tracer with Composite Reporter.
# CompositeReporter takes a list of other reporters and invokes them one by one
# Use ConsoleReporter to output span data to console.
composite_reporter = CompositeReporter(proxy_reporter, ConsoleReporter())   
tracer = WavefrontTracer(reporter=composite_reporter, application_tags=application_tag)


global_tags = [('global_key', 'global_val')]

# Create span1, return a newly started and activated Scope.
scope = tracer.start_active_span(
    	operation_name='span1',
        tags=global_tags,
        ignore_active_span=True,
        finish_on_close=True
)
span1 = scope.span
time.sleep(0.1)

# Create span2, span3 child of span1.
span2 = tracer.start_span(
    	operation_name='span2',
        references=opentracing.child_of(span1.context),
        tags=[('span2_key', 'span2_val')]
)
span2.log_kv({'foo': 'bar'})
span3 = tracer.start_span(
        operation_name='span3',
        child_of=span1,
        tags=[('span3_key', 'span3_val')]
)
time.sleep(0.2)
span2.finish()
time.sleep(0.1)
span3.finish()

# Create span4 follows from span3.
span4 = tracer.start_span(
        operation_name='span4',
        references=opentracing.follows_from(span3.context),
        tags=[('span4_key', 'span4_val')]
)
time.sleep(0.2)
span4.finish()

span5 = tracer.start_span(operation_name='span5')
time.sleep(0.1)
span5.finish()

time.sleep(0.1)

# Close the scope
scope.close()

# Close the tracer
tracer.close()
    

