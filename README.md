# jvmthreadparser
This project converts a JVM thread dump generated with jstack -l &lt;PID> to a pandas.DataFrame. The main goal is make data analysis easier.

Example:

```
c:\temp\jvmthreadparser>python
Python 3.5.3 |Anaconda custom (64-bit)| (default, Feb 22 2017, 21:28:42) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import jvmthreadparser.parser as jtp
>>> df = jtp.ope<PRESS TAB>
jtp.open_gzip( jtp.open_text(
>>> df = jtp.open_text('threads.txt')
>>> df.columns
Index(['DateTime', 'Thread', 'State'], dtype='object')
>>> df.State.value_counts()
TIMED_WAITING (PARKING)              181
TIMED_WAITING (ON OBJECT MONITOR)     55
RUNNABLE                              27
WAITING (ON OBJECT MONITOR)            4
TIMED_WAITING (SLEEPING)               3
Name: State, dtype: int64
>>> df.head()
             DateTime                                             Thread  \
0 2017-05-25 01:02:01  "Attach Listener" daemon prio=10 tid=0x0000000...
1 2017-05-25 01:02:01  "ajp-apr-8009-exec-129 ^ 25/05/2017 - 01:01:56...
2 2017-05-25 01:02:01  "ajp-apr-8009-exec-128 ^ 25/05/2017 - 01:02:01...
3 2017-05-25 01:02:01  "ajp-apr-8009-exec-127 ^ 25/05/2017 - 01:02:00...
4 2017-05-25 01:02:01  "ajp-apr-8009-exec-126 ^ 25/05/2017 - 01:01:58...

                     State
0                 RUNNABLE
1  TIMED_WAITING (PARKING)
2  TIMED_WAITING (PARKING)
3  TIMED_WAITING (PARKING)
4  TIMED_WAITING (PARKING)
>>>
```
