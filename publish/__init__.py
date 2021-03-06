# -*- coding: utf-8 -*-

from mako.template import Template
import time
import logging
import sanitizer
import config

module_logger = logging.getLogger("backwater.publish")

def publish(tmpl, outfile, entries, opt_template_values=None):
    """Using entries, publishes tmpl to outfile using Mako.
    
    opt_template_values must be a dictionary."""
    current_timestamp = time.strftime(config.ATOM_TIME_FORMAT, time.localtime())
    #template = Template(filename=tmpl, default_filters=['decode.utf8'])
    template = Template(filename=tmpl, output_encoding='utf-8')
    template_values = {
        'now':  current_timestamp, 
        'generator': config.BOT_NAME, 
        'generator_url': config.BOT_URL, 
        'generator_version': config.__version__, 
        'base_url': config.BASE_URL, 
        'feeds_url': config.FEEDS_URL, 
        'entries': entries
    }
    if opt_template_values is not None:
        template_values.update(opt_template_values)
    try:
        f = open(outfile, 'w')
        f.write(template.render(**template_values))
        f.close()
    except IOError:
        raise
    
    
