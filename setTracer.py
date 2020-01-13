
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
# Use ConsoleReporter to output span data to console
composite_reporter = CompositeReporter(proxy_reporter, ConsoleReporter())   


tracer = WavefrontTracer(reporter=composite_reporter, application_tags=application_tag)

print('tracer = '+tracer)

tracer.close()


