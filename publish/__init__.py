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
    template = Template(filename=tmpl)
    template_values = {
        'now':  current_timestamp, 
        'generator': config.BOT_USER_AGENT, 
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
    
    