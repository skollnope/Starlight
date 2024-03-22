from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

from  .. import constantsDef  as cstDef
from . import sharedDefinitions as sharedDef


class ActionGetLocaltime(Action):
    def name(delft) -> Text:
        return "action_get_localtime"
    
    async def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = f"it's {sharedDef.getLocalTime()}"

        dispatcher.utter_message(text=message)        
        return []