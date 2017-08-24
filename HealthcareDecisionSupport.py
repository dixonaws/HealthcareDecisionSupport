"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages reservations for hotel rooms and car rentals.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'BookTrip' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""

import json
import datetime
import time
import os
import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }

def close(fulfillment_state, message):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

# added message to this method, does it work? no
def delegate(session_attributes, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None

# --- End Helper Functions ---


# --- HealthcareDecisionSupport Intents ---

def healthcareDecisionSupport(intent_request):
    logger.debug("reached healthcareDecisionSupport intent method")

    # Receive the slots from the Lex chatbot and place the values into variables that match the slot name
    slots = intent_request['currentIntent']['slots']

    # Receive the session_attributes, or set to None if there are none
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # We call try_ex to safely access the dictionary object, knowing that some of the slots may not contain data
    logger.debug('healthcareDecisionSupport(): loading slot values...')
    PreferHSA = try_ex(lambda: slots['PreferHSA'])
    ExtremeSports = try_ex(lambda: slots['ExtremeSports'])
    WiseConsumer = try_ex(lambda: slots['WiseConsumer'])
    HighConsumer = try_ex(lambda: slots['HighConsumer'])
    TrackExpenses = try_ex(lambda: slots['TrackExpenses'])

    # test debug message
    logger.debug('PreferHSA={}'.format(PreferHSA))

    # When to display the welcome message? When no slots contain data AND we have invocationSource=DialogCodeHook
    if(intent_request['invocationSource'] == "DialogCodeHook") and (PreferHSA is None) and (ExtremeSports is None) and (WiseConsumer is None) and (HighConsumer is None) and (TrackExpenses is None):
        logger.debug("healthcareDecisionSupport: I received dialog code hook.")
        logger.debug('All slots appear to contain no data')

        # the delegate method works
        #return delegate(session_attributes, slots)

        #slot_to_elicit=str('PreferHSA')
        #message='Welcome to HMI HR Bot - HealthcareDecisionSupport v1.0'
        #return elicit_slot(session_attributes, intent_request['currentIntent']['name'],slots,slot_to_elicit, message)

    # if we fall through to this point, we consider the call a fulfillment request
    return close(
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'HermanMiller HealthcareDecisionSupport v1.0: I recommend you enroll into a high-deductible healthcare plan.'
        }
    )

# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    # We only support one intent at this time (so the dispatch method is only kept for good form)
    if (intent_name == 'HealthcareDecisionSupport'):
        return healthcareDecisionSupport(intent_request)

    logger.debug('Intent with name ' + intent_name + ' not supported')
    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    logger.debug('invocationSource={}'.format(event['invocationSource']))

    return dispatch(event)
