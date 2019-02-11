import logging
import coloredlogs

Tlog = logging.getLogger(__name__)
fh = logging.FileHandler('debug.log')
fieldStyle = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white',),
    programname=dict(color='cyan'),
    name=dict(color='blue'))
levelStyle = dict(
    spam=dict(color='green', faint=True),
    debug=dict(color='cyan'),
    verbose=dict(color='blue'),
    info=dict(),
    notice=dict(color='magenta'),
    warning=dict(color='yellow'),
    success=dict(color='green', bold=True),
    error=dict(color='red'),
    critical=dict(color='red', bold=True))
"""Mapping of log format names to default font styles."""
coloredlogs.install(level='DEBUG',
                    logger=Tlog,
                    datefmt='%H:%M:%S',
                    fmt='[%(levelname)s]%(asctime)s || %(message)s',
                    field_styles=fieldStyle, level_styles=levelStyle)
fh.setFormatter(logging.Formatter("[%(levelname)s]%(asctime)s || %(message)s"))
Tlog.addHandler(fh)
log = Tlog