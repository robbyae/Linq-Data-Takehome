# ASSUMPTIONS
# The application is stateless, so I can retry events without having to include context from previous or future events.
# The consumer-worker processes random inputs by multiplying them by 2
# To simulate failures, there is a random chance that the consumer-worker returns a failure

from collections import deque
import random
import time

class EventBus:
  def __init__(self):
    # Event bus queue
    self.queue = deque()
    # Dead letter queue (DLQ)
    self.dlq = deque()

  def send_event(self, event):
    self.queue.append(event)

  def acknowledge_failure(self, event):
    print(f"Failure acknowledged for event {event['id']}")
    event["retry_count"] += 1
    if event["retry_count"] <= 2: # Retry max twice
      print(f"Retrying event {event['id']} after delay")
      time.sleep(2)
      self.send_event(event) # return event to bus
    else:
      # send event to DLQ for manual review
      event["retry_count"] -= 1
      print(f"Sending event {event['id']} to DLQ")
      self.dlq.append(event)

class Producer:
  def __init__(self, event_bus):
    self.event_bus = event_bus
    self.event_id = 0

  # inital production
  def produce_event(self):
    self.event_id += 1
    event_data = random.randint(1, 100)
    event = {"id": self.event_id, "data": event_data, "retry_count": 0}
    print(f"Producing event {event['id']} with data {event['data']}")
    self.event_bus.send_event(event)

class Consumer:
  def __init__(self, event_bus):
    self.event_bus = event_bus

  def process_queue(self):
    while self.event_bus.queue:
      event = self.event_bus.queue.popleft()
      success = self.process_event(event)
      if not success:
        # retry processing
        self.event_bus.acknowledge_failure(event)

  def process_event(self, event):
    try:
      # Simulate processing with random chance of failure
      if random.choice([True, False]):
        raise ValueError("Processing error")
      result = event["data"] * 2  # processing
      print(f"Processed event {event['id']} with result {result}")
      return True
    except Exception as error:
      print(f"Failed to process event {event['id']}: {error}")
      return False

def Main():
  # Create bus, producer, consumer
  event_bus = EventBus()
  producer = Producer(event_bus)
  consumer = Consumer(event_bus)

  # Produce events
  for event in range(5):
    producer.produce_event()

  # Consume events
  consumer.process_queue()

  print("DLQ:", list(event_bus.dlq))

if __name__ == "__main__":
  Main()