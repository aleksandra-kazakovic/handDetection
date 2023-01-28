class CompartmentPickModel:
    def __init__(self, id, port_id, bin_type, compartment_id, creation_timestamp=None):
        self.id = id
        self.portId = port_id
        self.binType = bin_type
        self.compartmentId = compartment_id
        self.creationTimestamp = creation_timestamp