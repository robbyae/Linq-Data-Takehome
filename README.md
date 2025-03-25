# Linq-Data-Takehome

<h3>My Assumptions</h3>
• The application is stateless, so I can retry events without having to include context from previous or future events.<br><br>
• The consumer-worker processes random inputs by multiplying them by 2<br><br>
• To simulate failures, there is a random chance that the consumer-worker returns a failure

<h3>My approach:</h3>
• Create an application with event bus, producer, and consumer functions. Produce x events of random value (0,100), and double that value. Each event has a random chance to fail during processing, and events that fail twice are sent to a dead-letter queue for manual review.<br><br>
• This approach only works on stateless applications. Because I do not have access to external databases or event logs, I made the application stateless. This allows me to retry events without needing to include context from previous or future events.<br><br>
• I made the processor function atomic so no events are partially complete.<br><br>
• If I had access to external logs or databases, I could store the entire event history and implement a stateful application. This would allow me to retry a series of events in order to recalculate the result instead of just replaying a single event.<br><br>
• To scale to millions of events, I would decouple each component so each part of the systems can operate and scale independently. I would implement idempotency on my consumer function to remove the chance that events are processed more than once.
