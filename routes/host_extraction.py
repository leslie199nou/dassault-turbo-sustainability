import logging

from flask_openapi3 import APIBlueprint, Tag
from flask import current_app, send_from_directory, abort
from tools import export_to_json
from config import ConfigKeys
import jsonpickle
import logging
from tools import csv_import

from turbonomic import turbo_client, VirtualMachine as Vm, Host as Ht, Host


logger = logging.getLogger(__name__)

tag = Tag(name='Host', description="Read containers from Turbo, extract data and download them")
host_extraction = APIBlueprint('host_extraction', __name__, abp_tags=[tag], url_prefix='/hosts')
market_uuid=215698467690560;


def find_stat_by_name(key: str, data: dict) -> float:
    for stat in data:
        if stat['name'] == key:
            return (float(stat['value']), 0)[stat['value'] is None]
    return 0


@host_extraction.get('/export')
def index():
    conf = current_app.config

    client = turbo_client.TurboClient(conf.get(ConfigKeys.TURBONOMIC_URL.value),
                                      conf.get(ConfigKeys.TURBONOMIC_USER.value),
                                      conf.get(ConfigKeys.TURBONOMIC_PASS.value))

    csv_data = csv_import.get_csv_data()

    hts: list[Ht] = []
    vms: list[Vm]=[]
   
    print("------- Reading machines --------")
    resp_entities = client.list_machines_url()
    if resp_entities is not None:
        for entity in resp_entities:
            print(f"------- Reading host: {entity['uuid']}--------")
            ht = Ht(display_name=entity['displayName'], uuid=entity['uuid'])
            #ht.set_url_(entity['uuid'])
            # CSV mapping
            for csv_row in csv_data:
                if ht.display_name == csv_row[0].strip():
                    ht.display_name = csv_row[1].strip()

            stats_resp = client.get_stats_by_uuid(ht.uuid)
            if stats_resp is not None and len(stats_resp) > 0:
                #c.set_power(find_stat_by_name('Power', stats_resp[0]['statistics']))
                ht.set_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']))

            # reading VMs from consumers
            
            for consumer in entity['consumers']:
                if consumer['className'] == 'VirtualMachine':
                    print(f"------- Reading VM: {consumer['uuid']} --------")
                    vm = Vm(display_name=consumer['displayName'], uuid=consumer['uuid'])

                    ht.add_vm(consumer['uuid'])

                    sev_resp = client.get_search_by_uuid(ht.uuid)
                    vm.set_severity(sev_resp['severity'])

                    stats_resp = client.get_stats_by_uuid(ht.uuid)
                    if stats_resp is not None and len(stats_resp) > 0:
                        vm.set_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']))
                    vms.append(vm)

            hts.append(ht)

    file_name = export_to_json(jsonpickle.encode(hts, unpicklable=False), "u1")

    try:
        return send_from_directory(conf[ConfigKeys.APP_DOWNLOAD_DIRECTORY.value], file_name,
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)
    """
                    if consumer['className'] == 'VirtualMachine':
                        for vm in c.vm_list:  # Access the list of VirtualMachines in the Container
                            if vm.uuid == consumer['uuid']:
                                vm.set_host_uuid(ht.uuid)  # Call the set_host_uuid method on the VirtualMachine

    
            # reading VMs from consumers
            vms: list[Vm] = []
            for consumer in entity['consumers']:
                print(f"------- Reading VMs: {consumer['uuid']} --------")
                vm = Vm(display_name=consumer['displayName'], uuid=consumer['uuid'])

                sev_resp = client.get_search_by_uuid(vm.uuid)
                vm.set_severity(sev_resp['severity'])

                stats_resp = client.get_stats_by_uuid(vm.uuid)
                if stats_resp is not None and len(stats_resp) > 0:
                    vm.set_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']))

                ht.add_vm(consumer['uuid'])

            ht.vm_list = vms
            #h.set_avg_vm_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']), len(vms))
            containers.append(c)

 

            #c.set_avg_ht_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']), len(hts))
            #containers.append(c)
    
"""  
    
    file_name = export_to_json(jsonpickle.encode(containers, unpicklable=False), "u1")

    try:
        return send_from_directory(conf[ConfigKeys.APP_DOWNLOAD_DIRECTORY.value], file_name,
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)



