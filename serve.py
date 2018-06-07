 # Importing the libraries

import chatbot


def get_model_api():
    """Returns lambda function for api"""

    #model= chatbot.model


    def model_api(input_data):
        """
            Args:
            input_data: submitted to the API, raw string
             Returns:
            output_data: after some transformation, to be
                returned to the API
        """
       
        # 4. process the output
        output_data = chatbot.respond(input_data)
        # 5. return the output for the api
        return output_data

    return model_api
