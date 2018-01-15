=========================================================
Python parser for Interactive Brokers Flex XML statements
=========================================================

``ibflex`` is a Python library for converting brokerage statement data in
Interactive Brokers' Flex XML format into standard Python data structures,
so it can be conveniently processed and analyzed with Python scripts.

``ibflex`` is compatible with Python version 3.4+, and has no dependencies
beyond the Python standard library.

Installation
============
This should work:

::

    pip install git+https://github.com/csingley/ibflex

Flex Response Parser
====================
The primary facility provided is the ``FlexResponseParser`` class, which
parses Flex-format XML data into a standard Python ElementTree structure, then
converts the parsed data into normal Python types (e.g. datetime.datetime,
list) and exposes them through a nested dictionary whose structure corresponds
to that of the original Flex statements.

Usage example:

.. code:: python

    ofx.invstmtmsgsrsv1[0].invstmttrnrs.invstmtrs.invtranlist[-1].invsell.invtran.dttrade
    from ibflex.parser import FlexResponseParser
    parser = FlexResponseParser('/home/user/Downloads/2017-08.xml')
    response = parser.parse()
    stmt = response['FlexStatements'][0]
    trades = stmt['Trades']
    trade = {k: v for k, v in trades[0].items() if v is not None}
    

Flex Data Format
================
Generate Flex statements through `Interactive Brokers account management.`_ 

``ibflex`` is designed to parse whatever you throw at it without additional
configuration, with one major shortcoming: without providing additional
information out of band, it is difficult to distinguish US-style date
formats (MM/dd) from European-style date formats (dd/MM).

** DO YOURSELF A FAVOR AND CONFIGURE FLEX QUERIES TO USE ISO8601 DATE FORMATS
(YYYY-MM-dd) **


Resources
=========

* Interactive Brokers `Activity Flex Query Reference`_

.. _Interactive Brokers account management: https://gdcdyn.interactivebrokers.com/sso/Login 
.. _Activity Flex Query Reference: https://www.interactivebrokers.com/en/software/reportguide/reportguide.htm#reportguide/activity_flex_query_reference.htm
