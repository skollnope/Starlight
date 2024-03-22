from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

from  .. import constantsDef  as cstDef
from . import sharedDefinitions as sharedDef

class ActionGetCountryLocaltime(Action):
    def name(delft) -> Text:
        return "action_get_city_localtime"
    
    async def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message: str
        localtime = sharedDef.getLocalTime()

        # Check if location entity is present in tracker
        city = next(tracker.get_latest_entity_values(cstDef.ENTITY_CITY), None)
        if city is not None:
            message = f"I can't give you the current time in {city} (city) but it's {localtime} on you computer"
        else:
            message = f"it's {localtime}"

        dispatcher.utter_message(text=message)        
        return []