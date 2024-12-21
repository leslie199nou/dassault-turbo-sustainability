import logging

from flask_openapi3 import APIBlueprint, Tag
from flask import current_app, send_from_directory, abort
from tools import export_to_json
from config import ConfigKeys
import jsonpickle
import logging
from tools import csv_import

from turbonomic import turbo_client, VirtualMachine as Vm,  Host as Ht
from turbonomic.vm import VirtualMachineAction

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

    vms: list[Vm] = []

    # Read VMs first
    print("------- Reading VMs --------")
    resp_entities = client.list_machines_url()
    if resp_entities is not None:
        for entity in resp_entities:
            if entity['className'] == 'VirtualMachine':
                print(f"------- Reading VM: {entity['uuid']} --------")
                vm = Vm(display_name=entity['displayName'], uuid=entity['uuid'])

                stats_resp = client.get_stats_by_uuid(vm.uuid)
                if stats_resp is not None and len(stats_resp) > 0:
                    vm.set_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']))

                vms.append(vm)

    # Read hosts after VMs
    hts: list[Ht] = []
    print("------- Reading hosts --------")
    resp_entities = client.list_machines_url()
    if resp_entities is not None:
        for entity in resp_entities:
            if entity['className'] == 'Host':
                print(f"------- Reading host: {entity['uuid']}--------")
                ht = Ht(display_name=entity['displayName'], uuid=entity['uuid'])
                # CSV mapping
                for csv_row in csv_data:
                    if ht.display_name == csv_row[0].strip():
                        ht.display_name = csv_row[1].strip()

                stats_resp = client.get_stats_by_uuid(ht.uuid)
                if stats_resp is not None and len(stats_resp) > 0:
                    ht.set_energy(find_stat_by_name('Energy', stats_resp[0]['statistics']))

                hts.append(ht)

    file_name = export_to_json(jsonpickle.encode(vms + hts, unpicklable=False), "u1")

    try:
        return send_from_directory(conf[ConfigKeys.APP_DOWNLOAD_DIRECTORY.value], file_name,
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)
