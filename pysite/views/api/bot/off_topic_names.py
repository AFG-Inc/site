from flask import jsonify
from schema import And, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin


POST_SCHEMA = Schema({
    'name': And(
        str,
        len,
        lambda name: all(c.isalpha() or c == '-' for c in name),
        str.islower,
        lambda name: len(name) <= 96,
        error=(
            "The channel name must be a non-blank string consisting only of"
            " lowercase regular characters and '-' with a maximum length of 96"
        )
    )
})


class OffTopicNamesView(APIView, DBMixin):
    path = "/bot/off-topic-names"
    name = "bot.off_topic_names"
    table_name = "off_topic_names"

    @api_key
    def get(self):
        """
        Fetch all known off-topic channel names from the database.
        Returns a list of strings, the strings being the off-topic names.

        API key must be provided as header.
        """

        names = [
            entry['name'] for entry in self.db.get_all(self.table_name)
        ]
        return jsonify(names)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.params)
    def post(self, data):
        """
        Add a new off-topic channel name to the database.
        Expects the new channel's name as the `name` argument.
        The name must consist only of alphanumeric characters or minus signs,
        and must not be empty or exceed 96 characters.

        Data must be provided as params.
        API key must be provided as header.
        """

        if self.db.get(self.table_name, data['name']) is not None:
            response = {
                'message': "An entry with the given name already exists"
            }
            return jsonify(response), 400

        self.db.insert(
            self.table_name,
            {'name': data['name']}
        )
        return jsonify({'message': 'ok'})
