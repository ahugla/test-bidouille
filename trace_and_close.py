



import time
import opentracing
from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
import wavefront_sdk



time.sleep(0.1)

# Create span2, span3 child of span1.
span2 = tracer.start_span(
    	operation_name='span2',
        references=opentracing.child_of(span1.context),
        tags=[('span2_key', 'span2_val')]
)



span2.finish()


scope.close()

tracer.close()


