import os
import re
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('dashboard_hosts')

pre_cmd = "sudo bash -c \"source /root/openrc; "


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_nova_compute(host):
    cmd = pre_cmd + "ansible -m shell nova_compute -a \'reboot\' \""
    assert host.run_expect([0], cmd)


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_log_hosts(host):
    cmd = pre_cmd + "ansible -m shell log_hots -a \'reboot\' \""
    assert host.run_expect([0], cmd)
    verify_the_device_is_backup(host)


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_infra03(host):
    cmd = pre_cmd + "ansible -m shell <DEV#>-infra03 -a \'reboot\' \""
    assert host.run_expect([0], cmd)
    verify_the_device_is_backup(host)


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_infra02(host):
    cmd = pre_cmd + "ansible -m shell <DEV#>-infra02 -a \'reboot\' \""
    assert host.run_expect([0], cmd)
    verify_the_device_is_backup(host)


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_infra01(host):
    cmd = pre_cmd + "ansible -m shell <DEV#>-infra01 -a \'reboot\' \""
    assert host.run_expect([0], cmd)
    verify_the_device_is_backup(host)


@pytest.mark.jira('asc-228')
@pytest.mark.skip(reason='add skipped tests for asc-301')
def test_to_reboot_cinder_containers(host):
    cmd = pre_cmd + "ansible -m shell storage_hosts:!infra_hosts:!shared-infra_hosts:!os-infra_hosts -a \'reboot\' \""
    assert host.run_expect([0], cmd)
    verify_the_device_is_backup(host)

