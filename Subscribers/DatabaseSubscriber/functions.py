import os
from Subscribers.DatabaseSubscriber.Database.database import Database
from datetime import timedelta, datetime
from dotenv import load_dotenv
load_dotenv()

def add_pick_if_not_exist(compartmentPick):
    db = Database()
    picks = db.get_picks_by_port_id(compartmentPick.portId)
    if len(picks) == 0:
        db.add_pick(compartmentPick.portId,compartmentPick.binType,compartmentPick.compartmentId)
    else:
        last_pick = picks.pop()
        if last_pick.compartmentId == compartmentPick.compartmentId and last_pick.portId == compartmentPick.portId:
            picking_time = last_pick.creationTimestamp + timedelta(seconds=int(os.environ.get("MAX_SECONDS_DIFF")))
            if picking_time < datetime.now():
                db.add_pick(compartmentPick.portId,compartmentPick.binType,compartmentPick.compartmentId)
            print ("Vec postoji")
        else:
            db.add_pick(compartmentPick.portId,compartmentPick.binType,compartmentPick.compartmentId)