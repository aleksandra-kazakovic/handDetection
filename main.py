from Detection.handTrackingModule import handTrackingProcess
import multiprocessing
from Events.events_systems import Event
from Subscribers.DatabaseSubscriber.functions import add_pick_if_not_exist
import Configurations.helper as helper

if __name__ == "__main__":
    event = Event()
    event.register_event("Taking from compartment", add_pick_if_not_exist)
    config = helper.read_port_config()
    processList = []
    for portConfig in config.sections():
        portId = int(config[portConfig]['portId'])
        cameraInput = config[portConfig]['cameraInput']
        if cameraInput.isdigit():
            process = multiprocessing.Process(target=handTrackingProcess, args=(int(config[portConfig]['cameraInput']), portId, event))
        else:
            process = multiprocessing.Process(target=handTrackingProcess, args=(cameraInput, portId, event))
        processList.append(process)
        process.start()
    for process in processList:
        process.join()
