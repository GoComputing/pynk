.. PYNK documentation master file, created by
   sphinx-quickstart on Sat Jun  4 18:30:27 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive. https://keebfolio.netlify.app/

Welcome to PYNK's documentation!
================================

Welcome to the documentation of the PYNK keyboard firmware. Here you will find how to use the
firmware in a variety of keyboards. You can also learn how the firmware works. If you find this
firmware useful, please consider to contribute to it adding support to new keyboards or extending
its functionalities.

PYNK firmware
#############

**PYNK** (Python Neon Keyboard) is a firmware designed for custom keyboards writen in Python. One of its
highlights is the easy use of it, as all the main configuration is encapsulated into a JSON
file. This firmware is intended to be compatible with a large set of keyboards, including non-split
and split keyboards.

The goal of the firmware is to make easy to add support to new keyboards, standarizing the resources
of the keyboard. As an analogy, PYNK is like an operative system for keyboards, where all the resources
are managed by the firmware, and the user can program it with no knowing of what specific keyboard they
are using.

As first steps, take a look at the :ref:`quickstart` section, where a series of steps will show you
how to configure your keyboard, configure the firmware and upload it to your keyboard. Note that
these steps assumes that your keyboard is supported. Take a look at the :ref:`compatible keyboards <compatible-keyboards>`
section to check whenever your keyboard is supported.


Compatible keyborads
####################
.. _compatible-keyboards:


To make use of this firmware, you will need a keyboard with a microcontroller that supports
`CircuitPython <https://circuitpython.org/>`_. Most common compatible keyboards uses microcontroller
boards such us the `Pro Micro <https://deskthority.net/wiki/Arduino_Pro_Micro>`_, the
`nice!nano <https://nicekeyboards.com/nice-nano/>`_ or the `nRFMicro <https://github.com/joric/nrfmicro>`_.
Right now, PYNK firmware supports the following keyboards:

+---------------------------------------------------------------+--------------+---------------------+
| Keyboard                                                      | Versions     | Status              |
+===============================================================+==============+=====================+
| `Sofle <https://github.com/GoComputing/SofleKeyboard>`_       | nRFsofle     | Under development   |
+---------------------------------------------------------------+--------------+---------------------+

If you find your keyboard in the below list, you can make use of the configuration file from the
`configs` folder, so it would even easier to setup your keyboard. If you cannot find your keyboard,
consider contributing to this firmware adding support to your keyboard. To do so, refer to
:ref:`add-keyboard`.



Full table of contents
######################

.. toctree::
   :maxdepth: 2
   :caption: PYNK usage
   
   usage/quickstart

.. toctree::
   :maxdepth: 2
   :caption: Contributing
   
   extending/add_keyboard
