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
        message = current_time.strftime("%H:%M:%S")

        # Check if location entity is present in tracker
        country = tracker.get_latest_entity_values("location")
        if country:
            # Entity found, use the first value
            country = next(country)
            message += f" in {country}"  # Use f-string for clean formatting
        else:
            # Entity not found, handle the case
            message += " (your location)"  # Or any default message

        dispatcher.utter_message(text=message)        
        return []