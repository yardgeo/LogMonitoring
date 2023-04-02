# Following steps

1. Add functionality of saving producers and handlers state every n seconds to the persistent storage. That allows to
   restart from the pre-saved state in case of system crash so not reproduce big amount of data.
2. Supplement notification consumer logic to produce notification for all notification levels.
3. Add functionality of the multiple handlers of one class running. By now, only one instance of each handler can run,
   but it can cause issues in case of system scale. However, since async queue is a parameter for the class it is
   possible to change only internal handler logic to make system scalable.
4. Adopt the system to run in cloud environment. Add non-local storage producers. 