from ask_sdk_model import Intent
from ask_sdk_model.dialog import delegate_directive
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type

from deutschlandIntents import *
from bundeslandIntents import *
from landkreisIntents import *

app = Flask(__name__)
sb = SkillBuilder()


# API: https://api.corona-zahlen.org/docs/endpoints/germany.html#germany-2
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("Willkommen bei Coronazahlen Deutschland! "
                       "Wenn du Hilfe benötigst, sage 'Hilfe'"
                       )

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hallo!", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Moin! Ich hoffe dir geht es gut."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = speech_text = (
            "Du kannst mich nach der Inzidenz, den Todesfällen, den Fallzahlen oder den Genesenenzahlen "
            "für verschiedene Landkreise, Bundesländer oder ganz Deutschland fragen. "
            "Um zum Beispiel die 7-Tage-Inzidenz von Worms zu erfahren, sage 'wie hoch ist die inzidenz im landkreis worms'. "
            "Ich weiß auch wie viele Menschen in Deutschland einfach, zweifach und dreifach geimpft sind. "
            "Frage mich zum Beispiel 'Wie viele Menschen sind geboostert?'"
            )
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

        ##handler_input.response_builder.speak(speech_text).ask(
            ##speech_text).set_card(SimpleCard("Hilfestellung", speech_text))
       ## return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Machs gut und bleib gesund!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text =  "Ich glaube, da kann ich dir nicht weiterhelfen. Du kannst mich nach den Inzidenzen, Todesfällen, Genesenen, Neuinfektionen und Impfungen fragen."
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        app.logger.error(exception, exc_info=True)

        speech = "Sorry, ich habe gerade technische Schwierigkeiten. Versuch es später nochmal"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class yesIntentHandler(AbstractRequestHandler):
    """Handler for yes"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("yesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        destinationIntent = session_attr["destinationIntent"]

        print("destinationIntent: " + destinationIntent)

        return handler_input.response_builder.add_directive(delegate_directive.DelegateDirective(updated_intent=Intent(name=destinationIntent))).response


class noIntentHandler(AbstractRequestHandler):
    """Handler for no"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("noIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #clear session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["data"] = None

        return handler_input.response_builder.speak("Okay").set_should_end_session(
            False).response


#deutschlandIntents
sb.add_request_handler(DeutschlandInzidenzIntentHandler())
sb.add_request_handler(DeutschlandGesamtfallzahlIntentHandler())
sb.add_request_handler(DeutschlandGesamttodesfallzahlIntentHandler())
sb.add_request_handler(DeutschlandGesamtgenesenenzahlIntentHandler())
sb.add_request_handler(DeutschlandNeuinfektionenIntentHandler())
sb.add_request_handler(DeutschlandNeuGeneseneIntentHandler())
sb.add_request_handler(DeutschlandNeueTodesfaelleIntentHandler())
sb.add_request_handler(DeutschlandReproduktionszahlIntentHandler())
sb.add_request_handler(DeutschlandHospitalisierungszahlIntentHandler())
sb.add_request_handler(DeutschlandKrankenhauspatientenIntentHandler())

#impfungIntents
sb.add_request_handler(ErstimpfungenIntentHandler())
sb.add_request_handler(ZweitimpfungenIntentHandler())
sb.add_request_handler(BoosterimpfungenIntentHandler())

#bundeslandIntents
sb.add_request_handler(BundeslandInzidenzIntentHandler())
sb.add_request_handler(BundeslandNeuinfektionenIntentHandler())
sb.add_request_handler(BundeslandNeueTodesfaelleIntentHandler())
sb.add_request_handler(BundeslandNeuGeneseneIntentHandler())

#landkreisIntents
sb.add_request_handler(LandkreisInzidenzIntentHandler())
sb.add_request_handler(LandkreisNeuinfektionenIntentHandler())
sb.add_request_handler(LandkreisNeueTodesfaelleIntentHandler())
sb.add_request_handler(LandkreisNeuGeneseneIntentHandler())

#etc
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(yesIntentHandler())
sb.add_request_handler(noIntentHandler())

skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id=1, app=app)


@app.route('/', methods=['GET', 'POST'])
def invoke_skill():
    return skill_adapter.dispatch_request()


if __name__ == '__main__':
    app.run()
