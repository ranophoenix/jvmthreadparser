import gzip
import re
from datetime import datetime

import pandas as pd


"""Generate a pandas DataFrame based on a thread dump generated with: jstack -l <PID>."""

def open_gzip(filename):
    """Open a compacted thread dump (GZIP).
        Args:
            filename(str): file name of the thread dump.
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"].
    """
    with gzip.open(filename,'rt', encoding='UTF-8') as f:
         content = f.read()
         return parser(content)
       
def open_text(filename):
    """Open a thread dump in text format. 
        Args:
            filename(str): file name of the thread dump.
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"].
    """
    with open(filename,'rt', encoding='UTF-8') as f:
         content = f.read()
         return parser(content)

     
def parser(content):
    """Parse a thread dump generating a Pandas DataFrame.
        Args:
            content(str): Thread dump content.
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"].
    """
    dump_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\n([\s\S]+?JNI global references: \d+\n\n)', re.MULTILINE)
    dumps = [m.groups() for m in dump_pattern.finditer(content)]
     
    thread_list = []
    for dump_content in dumps:
       dump_date_time = datetime.strptime(dump_content[0].strip(),'%Y-%m-%d %H:%M:%S')
       dump_body = dump_content[1]
       #print(dump_body)
       #break
       thread_pattern = re.compile(r'("(:?[\s\S]+?\n\n\s{3}Locked[\s\S]+?\n\n|[\s\S]+?\n))', re.MULTILINE)
       threads = [m.groups() for m in thread_pattern.finditer(dump_body)]
       for thread in threads:       
           thread_body = thread[0].strip()
           state_pattern = re.compile(r'\s{3}java\.lang\.Thread\.State:\s(.+)')
           gc_state_pattern = re.compile(r'nid=0x\w{4} (.+)')
           state = '<NA>'
           state_match = state_pattern.search(thread_body)
           if state_match:
                state = state_match.group(1)
           else:
                gc_state_match = gc_state_pattern.search(thread_body)
                if gc_state_match:
                    state = gc_state_match.group(1)
                
           thread_list.append((dump_date_time, thread_body, state.strip().upper()))
    
    df = pd.DataFrame(thread_list, columns=["DateTime", "Thread", "State"])
    
    return df