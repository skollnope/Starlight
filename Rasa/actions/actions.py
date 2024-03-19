# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

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
        dispatcher.utter_message(text=message)
        return []
