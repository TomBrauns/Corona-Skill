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
districts = db["districts"]


class LandkreisInzidenzIntentHandler(AbstractRequestHandler):
    """Handler for Landkreis Inzidenz"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LandkreisInzidenzIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        landkreis = slots["Landkreis"].value
        districtData = getLandkreisData(landkreis)
        incidence = districtData["weekIncidence"]
        speech_text = "Die Inzidenz in " + landkreis + " beträgt " + formatOutput(incidence)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Landkreis Inzidenz", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class LandkreisNeuinfektionenIntentHandler(AbstractRequestHandler):
    """Handler for Landkreis Neuinfektionen"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LandkreisNeuinfektionenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        landkreis = slots["Landkreis"].value
        districtData = getLandkreisData(landkreis)
        newcases = districtData["delta"]
        newcases = newcases["cases"]
        speech_text = "In " + landkreis + " wurden gestern " + str(newcases) + " neue Corona-Fälle registriert."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Landkreis Neuinfektionen", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class LandkreisNeueTodesfaelleIntentHandler(AbstractRequestHandler):
    """Handler for Landkreis Neue Todesfaelle"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LandkreisNeueTodesfaelleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        landkreis = slots["Landkreis"].value
        districtData = getLandkreisData(landkreis)
        deaths = districtData["delta"]
        deaths = deaths["deaths"]
        speech_text = "In " + landkreis + " wurden gestern " + str(deaths) + " neue Corona-Tote registriert. "
        question = "Willst du hören, wie viele Menschen in " + landkreis + " seit gestern genesen sind?"

        saveSessionAttributes(handler_input, landkreis)["destinationIntent"] = "LandkreisNeuGeneseneIntent"  # followup intent after yesIntent if yesIntent is launched

        handler_input.response_builder.speak(speech_text + question).set_card(
            SimpleCard("Neue Todesfälle in " + landkreis, speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class LandkreisNeuGeneseneIntentHandler(AbstractRequestHandler):
    """Handler for Landkreis neu Genesene"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LandkreisNeuGeneseneIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        if "data" in session_attr:
            landkreis = session_attr["data"]
            session_attr["data"] = None

        else:
            slots = handler_input.request_envelope.request.intent.slots
            landkreis = slots["landkreis"].value

        districtData = getLandkreisData(landkreis)
        newrecovered = districtData["delta"]
        newrecovered = newrecovered["recovered"]
        speech_text = "In " + landkreis + " wurden gestern " + str(newrecovered) + " neu Genesene registriert"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Landkreis neu Genesene", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


def getLandkreisData(landkreis):
    flag: bool = False  # ags will be converted to string and loses leading 0, thats why we need flag
    result = districts.find_one({"district": landkreis})
    ags = result['ags']
    if ags < 9780: flag = True
    agsString = str(ags)
    if flag == True: agsString = "0" + agsString  #adds leading 0 to ags
    response = requests.get("https://api.corona-zahlen.org/districts/" + agsString).json()
    data = response["data"]
    districtData = data[agsString]
    return districtData