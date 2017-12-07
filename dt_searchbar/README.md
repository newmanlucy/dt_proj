# Duckietown search

This requires `lunr` for indexing. To install with `npm` run:

    $ npm install lunr

Assuming the markdown files are stored in `~/duckuments/docs`, you can create the index by running:

    $ ./make-index.sh ~/duckuments/docs

And then run a local server (port 8000 for example) and go to `localhost:8000/results.html`, and type a query into the searchbar.
