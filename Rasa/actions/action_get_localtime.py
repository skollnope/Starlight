from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

class ActionGetLocaltime(Action):
    def name(delft) -> Text:
        return "action_get_localtime"
    
    async def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.datetime.now()
        message = "It's " + current_time.strftime("%H:%M:%S")

        # Check if location entity is present in tracker
        country = next(tracker.get_latest_entity_values("country"), None)
        if country is not None:
            message += f" in {country}"  # Use f-string for clean formatting
        else:
            message += " on your computer"  # Or any default message

        dispatcher.utter_message(text=message)        
        return []