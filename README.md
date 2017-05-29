# jvmthreadparser
This project converts a JVM thread dump generated with jstack -l &lt;PID> to a pandas.DataFrame. The main goal is make data analysis easier.

Example:

```python
c:\temp\jvmthreadparser>python
Python 3.5.3 |Anaconda custom (64-bit)| (default, Feb 22 2017, 21:28:42) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import jvmthreadparser.parser as jtp
>>> df = jtp.ope
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
>>>
```
