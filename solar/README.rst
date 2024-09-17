
======
GeoSol
======

Save electricity by running CPU intensive jobs only during sunlight hours.

Combines a city to location database, a sunrise/sunset calculator, and a
process supervisor to save electricity.


Background
==========

Modern CPUs are becoming better and better and only drawing power when they are actually
doing work. Clock speeds and even core voltages are kept low unless needed. Conversely,
when running heavy tasks such as processing video, rendering 3D graphics, or running
simulations the system's power draw can increase dramatically.

For example, look at the whole-system power draw for two high-end desktop processors
as of November 2020:

============  ====  =========  ===========
CPU           Idle  100% load  Multiplier
============  ====  =========  ===========
AMD 5950X     64W   204W       **x3.2**
Intel 10900K  70W   336W       **x4.8**
============  ====  =========  ===========

The AMD system uses more than three times the power under load, while the Intel
uses almost five times more. Clearly it makes sense to try and run these
high-CPU jobs when electricity is available from a more renewable source.


Solar Power
===========

I have an array of solar panels on the roof of my home (and office). During daylight
hours they provide more power than I can use. The excess is sold to the grid
at a considerable discount. I buy power back from the grid during the night.
Therefore I try and run dish and clothes washers, hot water heaters, etc... during
the day whereever possible.

Another solution to the problem would be to invest in a battery storage system.
I have chosen to buy a bigger solar array instead, as I think it is more efficient --
at the society level.


Subprocess control
==================

Stop long-running computations at dusk, then resume them at dawn (or a few
hours before or after each):

.. code-block:: python

    import subprocess
    import signal
    import time

    p = subprocess.Popen(['mpg123', '-C', 'music.mp3'])
    time.sleep(3)
    print('stop')
    p.send_signal(signal.SIGSTOP)
    time.sleep(3)
    print('continue')
    p.send_signal(signal.SIGCONT)
    time.sleep(3)
    p.terminate()
