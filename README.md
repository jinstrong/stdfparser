# stdfparser
Automatically exported from code.google.com/p/stdfparser


This Repo is originally cloned from code.google.com/p/stdfparser, which is already pretty robust and full.
I modified/added some more functions so that it makes more meaning and reduces summary & report time:

1: fixed one bug in def _get_Nn:

\-    return (r, buf[1])

\+    return (r, buf[1:])

2: import Pandas to save data to DataFrame and dump to corresponding sheets of integrated excel file;

3: import Multithreading to run in parallel;

possible improvement:

1: further combine data to show in integrated way;

2: enhance argparse function so detailed processing parameters could be sent with terminal commands;


I am new to STDF (ATE) and I am all ears to hear any instruction as well as  discussion on related fields.

Thanks,

Jinqiang He

jinqiang.he@hotmail.com
