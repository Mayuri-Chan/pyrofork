Install Guide
=============

Being a modern Python framework, Pyrofork requires an up to date version of Python to be installed in your system.
We recommend using the latest versions of both Python 3 and pip.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Install Pyrofork
----------------

-   The easiest way to install and upgrade Pyrofork to its latest stable version is by using **pip**:

    .. code-block:: text

        $ pip3 install -U pyrofork

-   or, with :doc:`TgCrypto <../topics/speedups>` as extra requirement (recommended):

    .. code-block:: text

        $ pip3 install -U pyrofork tgcrypto

Bleeding Edge
-------------

You can install the development version from the git ``master`` branch using this command:

.. code-block:: text

    $ pip3 install -U https://github.com/Mayuri-Chan/pyrofork/archive/master.zip

Verifying
---------

To verify that Pyrofork is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. parsed-literal::

    >>> import pyrogram
    >>> pyrogram.__version__
    'x.y.z'

.. _`Github repo`: http://github.com/Mayuri-Chan/pyrofork
