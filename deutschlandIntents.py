import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from utilities import *


class DeutschlandInzidenzIntentHandler(AbstractRequestHandler):
    """Handler for Deutschland Inzidenz"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandInzidenzIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        response = requests.get("https://api.corona-zahlen.org/germany").json()
        incidence = response["weekIncidence"]
        speech_text = "Die 7-Tage Inzidenz in Deutschland beträgt " + formatOutput(incidence)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandGesamtfallzahlIntentHandler(AbstractRequestHandler):
    """Handler for Deutschland Gesamtfallzahl"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandGesamtfallzahlIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        fallzahl = response["cases"]
        fallzahlString = str(fallzahl)
        speech_text = "In Deutschland haben sich bis heute " + fallzahlString + " Menschen mit Covid-19 infiziert."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandGesamttodesfallzahlIntentHandler(AbstractRequestHandler):
    """Handler for Deutschland Gesamttodesfallzahl"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandGesamttodesfallzahlIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        todesfaelle = response["deaths"]
        todesfallzahlString = str(todesfaelle)
        speech_text = "In Deutschland sind bis heute " + todesfallzahlString + " Menschen mit Covid-19 gestorben"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandGesamtgenesenenzahlIntentHandler(AbstractRequestHandler):
    """Handler for gesamte Genesenenzahl Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandGesamtgenesenenzahlIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        response = requests.get("https://api.corona-zahlen.org/germany").json()
        genesenenzahl = response["recovered"]
        speech_text = "In Deutschland sind bis heute " + str(genesenenzahl) + " Covid-19-Infizierte genesen. "
        question = "Willst du auch wissen, wie viele Menschen die Infektion nicht überstanden haben?"

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["destinationIntent"] = "DeutschlandGesamttodesfallzahlIntent"

        handler_input.response_builder.speak(speech_text + question).set_card(
            SimpleCard("Gesamtgenesenenzahl Deutschland", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandNeuinfektionenIntentHandler(AbstractRequestHandler):
    """Handler for neue Faelle in Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandNeuinfektionenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        deltainfos = response["delta"]
        neueFallzahl = deltainfos["cases"]
        speech_text = "In Deutschland wurden gestern " + str(neueFallzahl) + " neue Corona-Fälle registriert."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandNeuGeneseneIntentHandler(AbstractRequestHandler):
    """Handler for neulich Genesene in Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandNeuGeneseneIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        deltainfos = response["delta"]
        neueGenesene = deltainfos["recovered"]
        speech_text = "In Deutschland wurden gestern " + str(neueGenesene)+ " neu Genesene registriert. "
        question = "Willst du wissen, wie viele Menschen in Deutschland insgesamt genesen sind?"

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["destinationIntent"] = "DeutschlandGesamtgenesenenzahlIntent"

        handler_input.response_builder.speak(speech_text + question).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandNeueTodesfaelleIntentHandler(AbstractRequestHandler):
    """Handler for neue Todesfälle in Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandNeueTodesfaelleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        deltainfos = response["delta"]
        neueTodesfallzahl = deltainfos["deaths"]
        speech_text = "In Deutschland wurden gestern " + str(neueTodesfallzahl) + " neue Todesfälle im Zusammenhang mit Covid-19 registriert. "
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandReproduktionszahlIntentHandler(AbstractRequestHandler):
    """Handler for Reproduktionszahl in Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandReproduktionszahlIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        rresponse = response["r"]
        rrate = rresponse["value"]
        round(rrate, 2)
        rincidenceString = str(rrate)
        rincidenceString = rincidenceString.replace('.', ',')
        speech_text = "Der R-Wert in Deutschland beträgt " + rincidenceString + ". "
        question = "Soll ich dir auch verraten, wie viele Menschen sich gestern infiziert haben?"

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["destinationIntent"] = "DeutschlandNeuinfektionenIntent"

        handler_input.response_builder.speak(speech_text + question).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandHospitalisierungszahlIntentHandler(AbstractRequestHandler):
    """Handler for Hospitalisierungszahl in Deutschland"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandHospitalisierungszahlIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/germany").json()
        hospitalisierungszahl = response["hospitalization"]
        hospitalisierungszahl = hospitalisierungszahl["incidence7Days"]
        hospitalisierungszahlString = str(hospitalisierungszahl)
        speech_text = "Die Hospitalisierungszahl in Deutschland beträgt " + hospitalisierungszahlString + "."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class ErstimpfungenIntentHandler(AbstractRequestHandler):
    """Handler for verabreichte Erstimpfungen"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ErstimpfungenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/vaccinations").json()
        data = response["data"]

        neueErstimpfungen = data["delta"]
        anzahlErstgeimpfte = data["vaccinated"]
        quoteErstgeimpfte = data["quote"]
        quoteErstgeimpfte = quoteErstgeimpfte * 100

        speech_text = "In Deutschland wurden gestern " + str(neueErstimpfungen) + " Erstimpfungen verabreicht. Damit liegt die Erstimpfungsquote bei " + formatOutput(quoteErstgeimpfte) + "%. Insgesamt sind in Deutschland " + str(anzahlErstgeimpfte) + " Menschen erstgeimpft."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class ZweitimpfungenIntentHandler(AbstractRequestHandler):
    """Handler for verabreichte Zweitimpfungen"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ZweitimpfungenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/vaccinations").json()
        data = response["data"]
        data = data["secondVaccination"]
        neueZweitimpfungen = data["delta"]
        anzahlZweitgeimpfte = data["vaccinated"]
        quoteZweitgeimpfte = data["quote"]
        quoteZweitgeimpfte = quoteZweitgeimpfte * 100

        speech_text = "In Deutschland wurden gestern " + str(neueZweitimpfungen) + " Zweitimpfungen verabreicht. Damit liegt die Impfquote bei " + formatOutput(quoteZweitgeimpfte) + "%. Insgesamt sind in Deutschland " + str(anzahlZweitgeimpfte) + " Menschen zweifach geimpft. "
        hint = "Du kannst mich auch speziell nach der Erstimpfungsquote oder Boosterquote fragen. Sage einfach 'Wie viele Menschen in Deutschland sind geboostert?'"
        handler_input.response_builder.speak(speech_text + hint).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class BoosterimpfungenIntentHandler(AbstractRequestHandler):
    """Handler for verabreichte Zweitimpfungen"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BoosterimpfungenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get("https://api.corona-zahlen.org/vaccinations").json()
        data = response["data"]
        data = data["boosterVaccination"]
        neueBoosterimpfungen = data["delta"]
        anzahlBoostergeimpfte = data["vaccinated"]
        quoteBoostergeimpfte = data["quote"]
        quoteBoostergeimpfte = quoteBoostergeimpfte * 100

        speech_text = "In Deutschland wurden gestern " + str(neueBoosterimpfungen) + " Boosterimpfungen verabreicht. Damit liegt die Boosterquote bei " + formatOutput(quoteBoostergeimpfte) + "%. Insgesamt sind in Deutschland " + str(anzahlBoostergeimpfte) + " Menschen geboostert."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DeutschlandKrankenhauspatientenIntentHandler(AbstractRequestHandler):
    """Handler for Krankenhauspatienten in Deutschland"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeutschlandKrankenhauspatientenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        response = requests.get("https://api.corona-zahlen.org/germany").json()
        krankenhauspatientenzahl = response["hospitalization"]
        krankenhauspatientenzahl = krankenhauspatientenzahl["cases7Days"]
        krankenhauspatientenzahlString = str(krankenhauspatientenzahl)
        speech_text = "In den letzten 7 Tagen kamen " + krankenhauspatientenzahlString + " Menschen mit Corona in deutsche Krankenhäuser."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response