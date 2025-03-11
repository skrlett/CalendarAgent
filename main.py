from client import client
from store import messages
from calendar_tools import process_calendar_request

if __name__ == "__main__":

    user_input = "Arrange Event for tomorrow with Alice and Bob to talk about the progress of the project"
    conf_1 = process_calendar_request(user_input=user_input)

    print(conf_1)

    user_input_2 = "Modify Event for tomorrow from 3pm to 4pm pst with Alice and Bob to talk about the progress of the project"
    conf_2 = process_calendar_request(user_input=user_input_2)

    print(conf_2)

    user_input_3 = "what is the capital of South Africa"
    conf_3 = process_calendar_request(user_input=user_input_3)

    print(conf_3)
