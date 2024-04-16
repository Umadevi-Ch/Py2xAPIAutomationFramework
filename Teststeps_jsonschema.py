#Step1:Get the response
# Step2:Create the JSon schema- https://www.jsonschema.net
# step3: Save the schema into the name .json file
# Step4: If we want to Validate the json schema https://www.jsonschemavalidator.net/
import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from src.constants.api_constants import APIConstants
from src.helpers.api_request_wrapper import post_request
from src.helpers.common_verification import verify_http_status_code, verify_json_key_for_not_null
from src.helpers.payload_manager import payload_create_booking
from src.utils.utils import Util

import allure
import pytest
import os
class TestcreatebookingJSONSchema(object):
    def load_schema(self,file_name):
        with open(file_name,'r')as file:
            return json.load(file)
    @pytest.mark.positive
    @allure.title("verify that create booking status and booking Id should not be null")
    @allure.description(
        "Creating a booking from the payload and verify that booking ID "
        "should not be null and status code should be 200 for the correct payload")
    def test_create_booking_schema(self):
         #URL, payload, headers

        response = post_request(url=APIConstants.url_create_booking(),
                                auth=None,
                                headers=Util().common_headers_json(),
                                payload=payload_create_booking(),
                                in_json=False)
        booking_id = response.json()["bookingid"]
        verify_http_status_code(response_data=response, expect_data=200)
        verify_json_key_for_not_null(booking_id)

       # Verify the response with schema.json that we have stored
        file_path =os.getcwd()+"/Create_booking_schema.json"
        schema = self.load_schema(file_name = file_path)
        try:
            validate(instance=response.json(),schema=schema)
        except ValidationError as e:
             print(e.message)
             pytest.fail("Failed:json schema error")
