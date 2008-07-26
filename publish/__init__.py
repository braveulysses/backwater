from mako.template import Template
import time
import logging
import sanitizer
import config

module_logger = logging.getLogger("backwater.publish")

def publish(tmpl, outfile, entries):
    current_timestamp = time.strftime(config.ATOM_TIME_FORMAT, time.localtime())
    template = Template(filename=tmpl)
    template_values = {
        'now':  current_timestamp, 
        'generator': config.BOT_USER_AGENT, 
        'base_url': config.BASE_URL, 
        'feeds_url': config.FEEDS_URL, 
        'entries': entries
    }
    try:
        f = open(outfile, 'w')
        f.write(template.render(**template_values))
        f.close()
    except IOError:
        raise
    
    