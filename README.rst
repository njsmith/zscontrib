zscontrib
=========

Extra misc ZS-related stuff that doesn't belong in the zs repository

ZS is here: https://github.com/njsmith/zs

These scripts are much hackier than the stuff in the zs repository
proper. They certainly assume UNIX, and almost certainly will only
work under Python 2.7, not anything earlier or later.


How to build .zs files from the Google Books v2 files
-----------------------------------------------------

Requirements: curl, python 2, gnu make, gnu sort

Nice to have: lzop, `pv <http://www.ivarch.com/programs/pv.shtml>`_

Install this package::

    pip install https://github.com/njsmith/zscontrib.git

Then generate a makefile for the subcorpus you want::

    python -m zscontrib.gbooks2 make-makefile LANGUAGE

where LANGUAGE is "eng-us-all" or whatever. This only takes a few
seconds, and creates a makefile called::

    google-books-LANGUAGE-20120701.make

This Makefile has targets like ``sorted-3gram``, which download and
sorts all the individual 3gram files, ``size-check-3gram`` which
double-checks that the downloaded files are similar in size to the
original ones (to make sure you didn't have a download failure that
will end up corrupting your .zs file!), and
``google-books-eng-us-all-20120701-3gram.zs``, which depends on those
first two, and creates the actual .zs file.

You probably want to start by doing something like::

  make -f google-books-LANGUAGE-20120701.make -j <something> sorted-3gram

where <something> can be determined empirically by trying a few values
and observing which ones crash your computer/cluster. (Each parallel
make will spawn a curl | gunzip | sort | gzip pipeline, and sort is
multithreaded, so you can get a ton of CPU/disk/network usage going
this way.)

Later, once you have the sorted files, you can run::

  make -f google-books-LANGUAGE-20120701.make google-books-LANGUAGE-20120701-3gram.zs

By default ``zs make`` will try to use all your CPUs, so it's probably
not a great idea to run this command at the same time as you're
running a big ``make -j`` on the same box.

Note that we use "0gram" to refer to what Google calls "totalcounts",
and "dependency" to refer to what Google calls "0gram". This is
because Google's terminology is bad and ours is better. We also
normalize the totalcounts file into the same format as the other
n-grams, with an empty string in the "ngram" column.

If you have multiple machines then you can work on the 1grams on one,
the 2grams on another, etc.

There are some variables at the top of the makefile that you might
well want to edit or otherwise override:

* ``ZS_OPTS`` are options to be passed to ``zs make``. You can
  pass --codec or -j here, for example.

* ``TMPDIR`` should probably point to a directory on *fast, local* disk,
  since it's where ``sort`` will scribble temporary files while
  working. Make sure it's big enough to handle the data that will be
  scribbled into it. (Basically this will be the size of a single
  Google-distributed ngram file, when compressed with lzop or whatever
  (see next item), times the number of parallel jobs you have running
  at once.)

* ``TMP_COMPRESS`` is the program that ``sort`` will use to
  compress/decompress these temporary files. ``lzop`` is a good
  choice. If you don't have lzop then you might want to make a little
  script like::

      #!/bin/sh
      exec gzip -1 "$@"

  and then point to that script here. Or if you have tons of space or
  are building a corpus for a small language then you can disable
  temporary compression altogether by editing the definition of
  ``SORT``.
