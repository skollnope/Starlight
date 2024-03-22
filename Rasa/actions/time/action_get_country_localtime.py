from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

from  .. import constantsDef  as cstDef
from . import sharedDefinitions as sharedDef

class ActionGetCountryLocaltime(Action):
    def name(delft) -> Text:
        return "action_get_country_localtime"
    
    async def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.datetime.now()
        message: str
        localtime = sharedDef.getLocalTime()

        # Check if location entity is present in tracker
        country = next(tracker.get_latest_entity_values(cstDef.ENTITY_COUNTRY), None)
        if country is not None:
            message = f"I can't give you the current time in {country} but it's {localtime} on you computer"
        else:
            message = f"it's {localtime}"

        dispatcher.utter_message(text=message)        
        return []