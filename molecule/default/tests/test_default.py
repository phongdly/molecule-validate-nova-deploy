import os
import re
import pytest
import json
import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('compute-infra_hosts')


# RPC10 manual test 1
def test_nova_force_config_drive_is_disabled(host):
    conf_files = ['/etc/openstack_deploy/user_variables.yml',
                  '/etc/ansible/roles/os_nova/defaults/main.yml']
    for conf_file in conf_files:
        if host.file(conf_file).contains('nova_force_config_drive'):
            cmd = "grep nova_force_config_drive " + conf_file
            output = host.check_output(cmd)
            # Fail test if there is 'nova_force_config_drive: True'
            assert not (re.search('nova_force_config_drive:\s+True', output))
            # Fail test if there is 'nova_force_config_drive: none'
            assert not (re.search('nova_force_config_drive:\s+none', output))
            # Verify the 'nova_force_config_drive' is set to be False
            assert (re.search('nova_force_config_drive:\s+False', output))


# RPC 10+ manual test 2a
def test_infra_nodes_removed_from_haproxy_hosts_config(host):
    config_file_path = '/etc/openstack_deploy/openstack_user_config.yml'
    with open(config_file_path, 'r') as config_file:
        data = yaml.load(config_file)
        haproxy_hosts = data['haproxy_hosts']
        for haproxy_host in haproxy_hosts:
            assert not (haproxy_host == 'compute-infra_hosts')
            assert not (haproxy_host == 'repo-infra_hosts')
            assert not (haproxy_host == 'shared-infra_hosts')
            assert not (haproxy_host == 'storage-infra_hosts')


# RPC 10+ manual test 2b
def test_infra_nodes_removed_from_haproxy_hosts_inventory(host):
    inventory_file_path = '/etc/openstack_deploy/openstack_inventory.json'
    data = json.load(open(host.file(inventory_file_path)))
    haproxy_hosts = data["haproxy_hosts"]["hosts"]
    for haproxy_host in haproxy_hosts:
        assert not (haproxy_host == 'compute-infra_hosts')
        assert not (haproxy_host == 'repo-infra_hosts')
        assert not (haproxy_host == 'shared-infra_hosts')
        assert not (haproxy_host == 'storage-infra_hosts')


# RPC 10+ manual test 2c
@pytest.mark.skip(reason='Only able to test on MNAIO environment')
def test_internal_load_balancer_vip_not_on_infra_node(host):
    # Expect that executing the command will return exit_code 1
    assert host.run_expect([1], 'ip a s br-mgmt')


# RPC 10+ manual test 2d
def test_load_balancer_vip_not_present(host):
    # Fail test if string 'br-mgmt' found in /etc/network/interfaces file
    assert not host.file('/etc/network/interfaces').contains('br-mgmt')


# RPC 10+ manual test 2e
@pytest.mark.skip(reason='Only able to test on MNAIO environment')
def test_haproxy_service_not_running(host):
    output = host.check_output('service haproxy status')
    assert (re.search('Active:\s+inactive', output))


# RPC 10+ manual test 2f
@pytest.mark.skip(reason='Only able to test on MNAIO environment')
def test_haproxy_packages_purged(host):
    # Expect that executing the command will return exit_code 1
    assert host.run_expect([1], 'dpkg -l | grep haproxy')
