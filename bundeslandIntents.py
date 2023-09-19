import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from pymongo import MongoClient
from utilities import *

client = MongoClient(port=27017)
db = client.local
states = db["states"]

class BundeslandInzidenzIntentHandler(AbstractRequestHandler):
    """Handler for Inzidenz Bundesland"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BundeslandInzidenzIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #get bundesland
        slots = handler_input.request_envelope.request.intent.slots
        bundesland = slots["bundesland"].value

        saveSessionAttributes(handler_input, bundesland)["destinationIntent"] = "BundeslandNeuinfektionenIntent"    #followup intent after yesIntent if yesIntent is launched

        data = getBundeslandData(bundesland)
        incidence = data["weekIncidence"]
        speech_text = "Die 7-Tage-Inzidenz in " + bundesland + " beträgt " + formatOutput(incidence) + ". Willst du noch mehr Informationen zur Corona-Lage in " + bundesland + "?"

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.set_card(SimpleCard("Inzidenz Bundesland", speech_text)).set_should_end_session(False).response


class BundeslandNeuinfektionenIntentHandler(AbstractRequestHandler):
    """Handler for Neuinfektionen Bundesland"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BundeslandNeuinfektionenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        if "data" in session_attr:
            bundesland = session_attr["data"]
            session_attr["data"] = None
        else:
            slots = handler_input.request_envelope.request.intent.slots
            bundesland = slots["bundesland"].value

        data = getBundeslandData(bundesland)
        delta = data["delta"]
        cases = delta["cases"]
        speech_text = "In " + bundesland + " wurden gestern " + str(cases) + " neue Corona-Fälle registriert."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Inzidenz Bundesland", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class BundeslandNeueTodesfaelleIntentHandler(AbstractRequestHandler):
    """Handler for Neue Todesfälle Bundesland"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BundeslandNeueTodesfaelleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        bundesland = slots["bundesland"].value
        data = getBundeslandData(bundesland)
        delta = data["delta"]
        deaths = delta["deaths"]
        speech_text = "In " + bundesland + " wurden gestern " + str(deaths) + " neue Corona-Tote registriert."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Neue Todesfälle Bundesland", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class BundeslandNeuGeneseneIntentHandler(AbstractRequestHandler):
    """Handler for Neu Genesene Bundesland"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BundeslandNeuGeneseneIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        bundesland = slots["bundesland"].value
        data = getBundeslandData(bundesland)
        delta = data["delta"]
        recovered = delta["recovered"]
        speech_text = "In " + bundesland + " wurden gestern " + str(recovered) + " neu Genesene registriert."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Neue Todesfälle Bundesland", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


def getBundeslandData(bundesland):
    print("slot: " + str(bundesland))
    databaseData = states.find_one({"state": bundesland})
    stateAcronym = databaseData['acronym']
    print("acronym: " + stateAcronym)
    response = requests.get("https://api.corona-zahlen.org/states/" + stateAcronym).json()
    data = response["data"]
    data = data[stateAcronym]
    return data