Module qfly.parallel
====================

Classes
-------

`MultipleError(errors)`
:   Exception class to collect several errors in a single object.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`parallel(*managers)`
:   Concurrently start and stop serveral context managers in different
    threads.
    
    Typical usage::
    
        with parallel(Foo(), Bar()) as managers:
            foo, bar = managers
            foo.do_something()
            bar.do_something()