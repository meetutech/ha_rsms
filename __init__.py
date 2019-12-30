import asyncio
import logging
import os
import json

from homeassistant.core import Event

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def rsms_stop(hass, entity_id=None):
    """Stop RSMS"""
    if hass.data[DOMAIN]['proc'] is not None:
        hass.data[DOMAIN]['proc'].terminate()
        hass.data[DOMAIN]['proc'] = None

async def rsms_start(hass, entity_id=None):
    """Event Start"""
    if hass.data[DOMAIN]['proc'] is None:
        rsms_client = {
            'name': hass.data[DOMAIN]['config']['client_identity'],
            'server-address': \
                hass.data[DOMAIN]['config']['server_address'] + ':' + 
                str(hass.data[DOMAIN]['config']['server_port']),                    
            'server-password': hass.data[DOMAIN]['config']['password']}
        rsms_config = {'clients': {'rsms-ha-local': rsms_client}}
        j = json.dumps(rsms_config, indent=4)
        f = open(hass.config.path('rsms_bin/etc/rsms.config'), 'w')
        print(j, file=f)
        f.close()

        # start a task
        os.putenv("HASS_CONFIG_PATH", hass.config.path())
        drun = asyncio.create_subprocess_shell(
            'curl -o- -LS https://rsms.meetutech.com/script/rsmsmgr-run.sh 2>/dev/null | bash')
        hass.data[DOMAIN]['proc'] = await drun

@asyncio.coroutine
async def async_setup(hass, config):

    """Set up the Reversed Stream Service Platform."""
    os.putenv("HASS_CONFIG_PATH", hass.config.path())

    # Initialize the cache data
    hass.data[DOMAIN] = {'proc': None, 'config': {}}

    """Install RSMS."""
    async def rsms_install():
        dproc = await asyncio.create_subprocess_shell(
            'curl -o- -LS https://rsms.meetutech.com/script/rsmsmgr-install.sh 2>/dev/null | bash')
        if dproc.returncoode == 1:
            hass.data[DOMAIN]['config']['message'] = 'Install rsmsmgr failed'
        else:
            hass.data[DOMAIN]['config']['installation'] = root_path + '/bin/rsmsmgr'

    proc = await asyncio.create_subprocess_shell(
        'curl -o- -LS https://rsms.meetutech.com/script/rsmsmgr-init.sh 2>/dev/null | bash', 
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    if stdout:
        conf = json.loads(stdout.decode())
        hass.data[DOMAIN]['config']['installation'] = conf['installed']
        hass.data[DOMAIN]['config']['server_address'] = conf['server']
        hass.data[DOMAIN]['config']['server_port'] = conf['port']
        hass.data[DOMAIN]['config']['client_identity'] = conf['client']
        hass.data[DOMAIN]['config']['password'] = conf['password']
        hass.data[DOMAIN]['config']['qrcode'] = conf['qrcode']
    else:
        return False

    if hass.data[DOMAIN]['config']['installation'] == 'Not Installed':
        await rsms_install()

    # Start the rsms
    await rsms_start(hass)
    _LOGGER.info('rsms started, scan qrcode: ' + hass.data[DOMAIN]['config']['qrcode'])
    # hass.states.async_set(DOMAIN + '.state', True)
    hass.components.persistent_notification.async_create(
        '![wechat](' + hass.data[DOMAIN]['config']['qrcode'] + ')', 
        'MeetU RSMS',
        DOMAIN + ".rsms.state"
        )

    return True
