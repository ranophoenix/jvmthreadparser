import gzip
import re
from datetime import datetime

import pandas as pd


"""Generate a pandas DataFrame based on a thread dump generated with: jstack -l <PID>."""

def open_gzip(filename, load_thread_content = True):
    """Open a compacted thread dump (GZIP).
        Args:
            filename(str): file name of the thread dump.
            load_thread_content(bool)
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"]
            or pd.DataFrame with columns=["DateTime", "State"] if load_thread_content == False.
    """
    with gzip.open(filename,'rt', encoding='UTF-8') as f:
         return parser(f, load_thread_content)
       
def open_text(filename, load_thread_content = True):
    """Open a thread dump in text format. 
        Args:
            filename(str): file name of the thread dump.
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"]
            or pd.DataFrame with columns=["DateTime", "State"] if load_thread_content == False.
    """
    with open(filename,'rt', encoding='UTF-8') as f:
         return parser(f, load_thread_content)

     
def parser(file, load_thread_content = True):
    """Parse a thread dump generating a Pandas DataFrame.
        Args:
            f(File Object): Pointer to a thread dump file.
        Returns: 
            pd.DataFrame with columns=["DateTime", "Thread", "State"]
            or pd.DataFrame with columns=["DateTime", "State"] if load_thread_content == False.
    """
    thread_list = []
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    thread_content = ""

    def add_thread():
        state = _get_thread_state(thread_content)
        if load_thread_content:
            thread_list.append((dump_date_time, thread_content.strip(), state.strip()))           
        else:
            thread_list.append((dump_date_time, state.strip()))           

    for line in file:
        if date_pattern.match(line):
            dump_date_time = datetime.strptime(line.strip(),'%Y-%m-%d %H:%M:%S')
        elif line.strip() == "" or line[0:4] == 'Full':
            pass
        elif line[0] == '"':
            if thread_content != "":
                add_thread()
            thread_content = line                            
        elif line[0:3] == 'JNI':
            add_thread()
            thread_content = ""
        else:
            thread_content += line                                   
    if load_thread_content:                  
        df = pd.DataFrame(thread_list, columns=["DateTime", "Thread", "State"])
    else:
        df = pd.DataFrame(thread_list, columns=["DateTime", "State"])
    
    return df
    
def _get_thread_state(thread_content):
    state_pattern = re.compile(r'\s{3}java\.lang\.Thread\.State:\s(.+)')
    gc_state_pattern = re.compile(r'nid=0x\w{4} (.+)')
    state = '<NA>'
    state_match = state_pattern.search(thread_content)
    if state_match:
        state = state_match.group(1)
    else:
        gc_state_match = gc_state_pattern.search(thread_content)
        if gc_state_match:
            state = gc_state_match.group(1)            
            
    return state.upper()
    