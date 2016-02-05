"""
Very simple Flask web site, with one page
displaying a map.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from math import modf


import json
import logging

###
# Globals
###

app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

POI = "static/POI.txt"

###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/map")
def index():
  app.logger.debug("Main page entry")
  if 'poi' not in flask.session:
      app.logger.debug("Processing raw POI file")
      raw = open(POI)
      flask.session['poi'] = process(raw)
  return flask.render_template('map.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("map")
    return flask.render_template('page_not_found.html'), 404
 
#################
#
# Functions used within the templates
#
#################

def process(raw):
    """
    Line by line processing of file
    """
    field = None
    entry = { }
    finalContent = [ ]
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                "Split into |{}|".format("|".join(parts)))

        if field == "place":
            if entry:
                finalContent.append(entry)
                entry = { }
            entry['address'] = ""
            entry['phone'] = ""
            entry['place'] = content
            print(field + ": " + content + "\n")

        elif field == 'address' or field == 'phone':
            entry[field] = content
            print(field + ": " + content + "\n")

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        finalContent.append(entry)

    return finalContent



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
