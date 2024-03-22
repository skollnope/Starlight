from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

import constantsDef  as cstDef

class ActionGetLocaltime(Action):
    def name(delft) -> Text:
        return "action_get_localtime"
    
    async def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.datetime.now()
        message: str
        localtime = current_time.strftime("%H:%M:%S")

        # Check if location entity is present in tracker
        country = next(tracker.get_latest_entity_values(cstDef.ENTITY_COUNTRY), None)
        if country is not None:
            message = f"I can't give you the current time in {country} but it's {localtime} on you computer"
        else:
            message = f"it's {localtime}"

        dispatcher.utter_message(text=message)        
        return []