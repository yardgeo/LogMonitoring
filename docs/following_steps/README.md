# Following steps

## Edge cases handling

1. Handle the case when a new log line does not correlate to the file header,
   that includes:
    1. Invalid number of columns. In that case it is not obvious which column
       is redundant.
        1. Invalid number of the delimiter symbol.
        2. Invalid placement of the delimiter symbol.
    2. Abnormal values. For example, request code status is an integer field
       for the program. But in a real-world scenario there is a set of possible
       code statuses.
2. Handle duplicate logs. If one log is duplicated two or more times, that may
   affect handler logic.
3. Create a new notification in case there are no new logs for a long time. (More
   than 2 minutes)
4. Supplement notification consumer logic to produce notification for all
   notification levels.

## Steps for scaling

1. Add functionality of saving producers and handlers state every n seconds to
   the persistent storage. That allows it to restart from the pre-saved state in
   case of system crash so not reprocess a large amount of data.
2. Add functionality of the multiple handlers of one class running. By now,
   only one instance of each handler can run, but it can cause issues in case
   of system scale. However, since async queue is a parameter for the class it
   is possible to change only internal handler logic to make the system scalable.
3. Add connectors for message brokers such as Kafka or RabbitMQ. These
   connectors can be used as sources of logs/events for log producers and can
   be used for notification delivery by notification producers.
4. Adopt the system to run in a cloud environment. Add non-local storage
   producers. 