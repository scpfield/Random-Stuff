# Random-Stuff
A repository for various things

CheckMemory.py  

Implements a decorator / annotator that uses the python tracemalloc package to track the heap usage of functions that are annotated by it.  Further information is in the comments in the file.  It includes a test target function that intentionally creates a memory leak.  The annotator function is not in a production-ready state, this is just for demonstration and what I did to learn how to make annotators.  I think they are perfect for this type of thing because it eliminates the need to pepper all your code with calls to external instrumentation modules for measuring performance.  Much cleaner to use an annotator because then all you need is to add:  "@CheckMemory" decorator to whichever functions you want to measure, and it just works and no messy code to add in your functions.  The CheckMemory.py file should just run without any arguments or configuration with the sample function it has that leaks 1MB of memory.


list_comprehension.py

Examples of it.
