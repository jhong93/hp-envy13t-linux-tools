#!/usr/bin/env python3

import time
from subprocess import check_output, check_call


AUDIO_FIX_SERVICE = 'fix-volume-ctrl'


def check_audio_fix():
    """Make sure that the quad speakers are configured"""
    print('Check: {}'.format(AUDIO_FIX_SERVICE))
    res = check_output(
        ['service {} status | cat'.format(AUDIO_FIX_SERVICE)],
        shell=True)
    if 'Active: active (running)' not in str(res):
        raise Exception('{} is not running'.format(AUDIO_FIX_SERVICE))
    else:
        print('Ok: {}'.format(AUDIO_FIX_SERVICE))


UNDERVOLT_SERVICE = 'iuvolt'
UNDERVOLT_SERVICE_TIMEOUT = 120
UNDERVOLT_SERVICE_RETRY_INTERVAL = 5


def check_undervolt():
    """Make sure that the undervolt offsets have been set"""
    print('Check: {}'.format(UNDERVOLT_SERVICE))

    def run_check():
        res = check_output(
            ['service {} status | cat'.format(UNDERVOLT_SERVICE)],
            shell=True)
        if '(code=exited, status=0/SUCCESS)' not in str(res):
            raise Exception('{} exited with error'.format(UNDERVOLT_SERVICE))

    start_time = time.time()
    while True:
        try:
            run_check()
            break
        except Exception:
            if time.time() - start_time > UNDERVOLT_SERVICE_TIMEOUT:
                print('exceeded {} timeout ({}s)'.format(
                    UNDERVOLT_SERVICE,
                    UNDERVOLT_SERVICE_TIMEOUT
                ))
                raise
            else:
                print('{} not ready. Retrying in {}s'.format(
                    UNDERVOLT_SERVICE,
                    UNDERVOLT_SERVICE_RETRY_INTERVAL
                ))
                time.sleep(UNDERVOLT_SERVICE_RETRY_INTERVAL)

    print('Ok: {}'.format(UNDERVOLT_SERVICE))


def check_bbswitch():
    """Make sure the nvidia gpu is disabled"""
    print('Check: bbswitch')
    res = check_output(['cat', '/proc/acpi/bbswitch'])
    if '0000:01:00.0 OFF' not in str(res):
        raise Exception('bbswitch failed to disable the GPU')
    else:
        print('Ok: bbswitch')


def main():
    try:
        check_bbswitch()
        check_audio_fix()
        check_undervolt()
    except Exception as e:
        check_call([
            'notify-send',
            str(e),
            'Run "systemctl status --user envy13t-check" for more details'])
        raise

    print('All services are ok.')
    check_call([
        'notify-send',
        'All envy13t services started successfully',
        'Run "systemctl status --user envy13t-check" for more details'])


if __name__ == '__main__':
    main()
