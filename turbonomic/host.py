
def convert_to_carbon_emission(energy: float) -> float:
    # results will be in KILO
    # pue: Private Cloud Power Usage Effectiveness (average value)
    # pcef: Private Cloud Emissions Factor (value for France - IEA - ENVIZI emission factor)
    # pre: Percent Renewable Energy
    pue = 1.67
    pcef = 0.0000514
    pre = 0
    return energy*(pue/1000)*pcef*((100 - pre)/100)*1000

def convert_to_avg_VM_energy(energy: float, vm_nb: float) -> float:
    if vm_nb is not None and vm_nb > 0:
        avg_energy_vm = energy / vm_nb
    else:
        avg_energy_vm = 0
    return avg_energy_vm

def convert_to_energy_intensity(energy: float) -> str:
    intensity="LOW"
    if energy is None or energy < 30:
        intensity="LOW"
    elif 30 <= energy < 60:
        intensity="MEDIUM"
    elif energy >= 60:
        intensity="HIGH"
    else :
        intensity="LOW"
    return intensity

def set_turbo_host_url(uuid: str) -> str:
    return "https://turbonomic.public.p120.cesc.nca.ihost.com/app/#/view/main/"+uuid


class VirtualMachine:
    display_name: str
    uuid: str
    severity: str
    #power_value: float
    energy_value: float
    energy_intensity: str
    #carbon_emissions: float
    #energy_VM_avg: float

    def __init__(self, display_name, uuid):
        self.uuid = uuid
        self.display_name = display_name

    def set_energy(self,  energy_value):
        self.energy_value = energy_value
        self.energy_intensity = convert_to_energy_intensity(self.energy_value)
        #self.energy_consumption = convert_to_carbon_emission(self.power_value)

    def set_severity(self, severity: str):
        self.severity = severity.upper()

    def set_host_uuid(self, host_uuid: str):
        self.host_uuid = host_uuid


class Host:
    display_name: str
    uuid: str
    severity: str
    power_value: float
    energy_value: float
    carbon_emissions: float
    energy_VM_avg: float
    vm_list: list[VirtualMachine] = []
    energy_intensity: str
    url: str
    

    def __init__(self, display_name, uuid, severity: str ):
        self.uuid = uuid
        self.severity = severity.upper()
        self.display_name = display_name
        

    #def set_power(self,energy_value):
        #self.power_value = power_value
        

    def set_energy(self, energy_value):
        self.energy_value = energy_value
        self.carbon_emissions= convert_to_carbon_emission(self.energy_value)
        self.energy_intensity = convert_to_energy_intensity(self.energy_value)
        
    
    def set_avg_vm_energy(self, energy_value,vm_nb):
        self.energy_VM_avg = convert_to_avg_VM_energy(energy_value, vm_nb)

    def set_url_host(self, uuid):
        self.url = set_turbo_host_url(uuid)

    def set_severity(self, severity: str):
        self.severity = severity.upper()

    def add_vm(self, vm): 
        self.vm_list.append(vm)
        print("adding vm" + vm+ " to " + self.display_name)


class HostAction:
    className: str
    actionType: str
    display_name: str
    uuid: str
    energy_value: float
    carbon_emissions: float
    energy_intensity: str

    def __init__(self, display_name, uuid,className, actionType ):
        self.uuid = uuid
        self.display_name = display_name
        self.actionType = actionType
        self.className = className

    def set_energy(self, energy_value):
        self.energy_value = energy_value
        self.carbon_emissions= convert_to_carbon_emission(self.energy_value)
        self.energy_intensity = convert_to_energy_intensity(self.energy_value)