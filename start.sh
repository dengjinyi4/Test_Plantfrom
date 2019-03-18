#!/bin/sh
gunicorn  show:app -b 0.0.0.0:21312