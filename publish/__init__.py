from mako.template import Template
import logging
import sanitizer
import config

module_logger = logging.getLogger("backwater.publish")

def publish(tmpl, outfile, entries):
    template = Template(filename=tmpl)
    template_values = {
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
    
    