# -*- coding: utf-8 -*-

import ask_sdk_core.utils as ask_utils
import requests
import json

#from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hi what do you want to know"
        reprompt_text = "anything else you wanna know?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class CallAPIIntentHandler(AbstractRequestHandler):
    """Handler for CallAPIIntent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CallAPIIntent")(handler_input)

    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        query = slots["sth"].value
        order = slots["good_bad"].value
        if (order=="good"):
            ord = 1
        else:
            ord = 0
        # search top 3 related articles with the query
        IPv4_adress = "3.125.19.179" # glove.6B.50d
        # IPv4_adress = "3.122.223.164" # sized-down w2v model
        url = f"http://{IPv4_adress}:8000/predict"
        data = {"query":query}
        
        r = requests.post(url, data = json.dumps(data))
        response = r.json()

        query = str(data["query"])
        headlines1 = str(response["Headlines"][0])
        headlines2 = str(response["Headlines"][1])
        headlines3 = str(response["Headlines"][2])
        
        # semantic analysis for each headline. order==1: positive-->negative; otherwise: negative-->positive
        IPv4_adress = "3.123.254.31" 
        url = f"http://{IPv4_adress}:8000/predict"
        data = {"headlines":[headlines1, headlines2, headlines3], "order":ord}
        r = requests.post(url, data = json.dumps(data))
        response = r.json()

        headlines1 = str(response["ordered_articles"][0])
        headlines2 = str(response["ordered_articles"][1])
        headlines3 = str(response["ordered_articles"][2])
        
        # hear the good one first
        if (order=="good"):
            speak_output = f"For news related to: {query}, the better one is {headlines1}.\n The worse one is {headlines3}"
        # hear the bad one first
        else:
            speak_output = f"For news related to: {query}, the worse one is {headlines1}.\n The better one is {headlines3}"

        # speak_output = "That model predicted 0 "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CallAPIIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) 

lambda_handler = sb.lambda_handler()