# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response= requests.get("https://api.covid19india.org/data.json").json()

        # print(response)
        entities=tracker.latest_message['entities']    #extracting the entities from the latest message what triggered this action
        print('latest message : ',entities)
        states=[];result=[]
        for e in entities:
            if(e['entity'].lower()=='state'):
                if(e['value'].lower()=='india'):
                    states.append('Total')
                else:
                    states.append(e['value'])        #one chat may have multiple entities, therefore collecting them in a list.

        print(states)
        if(states):            #if states list is not empty then process this block
            for data in response['statewise']:  #we're only interested in the statewise data from the response data.
                result+=[data for i in states if(data['state']==i.title())]    #getting the respective data for the interested entities.
                # print('#',data['state'],'    ',states)
            # print(result)
            for state_data in result:
                [dispatcher.utter_message(text=str(info)+' : '+str(state_data[info])) for info in ['active','confirmed','deaths','recovered','lastupdatedtime','state','statenotes']]
                dispatcher.utter_message(text='-'*100)
                # dispatcher.utter_message(text="Hello from corona tracker!"+str(i))
        else:
            dispatcher.utter_message(text='Please try again with correct state')
        return []
