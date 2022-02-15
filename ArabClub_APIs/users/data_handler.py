from __future__ import annotations

from typing import Any

from users.models import FirstNameAndLastName
from users.serializers import UpdateNamesSerializer, UpdateUserSerializer


class UpdateData:
    AlLow_Serializer = {
        "person_info": UpdateNamesSerializer,
        "basic": UpdateUserSerializer
    }
    Allow_Model = {}

    @classmethod
    def get_serializer(cls, key):
        return cls.AlLow_Serializer[key]

    def __init__(self, data, user=None):
        self.data = data
        self.user = user
        self.data_map = {
            "person_info": "person_info",
            "basic": "basic"
        }
        self.serializer_key = None
        self.serializer = None
        self.errors = None

    def get_model_key(self, map_key) -> ValueError | Any:
        try:
            return self.data_map[map_key]
        except KeyError:
            return ValueError('[Error 02]: Key Not Found get_model_key() 20 ')

    def save_data(self):
        for key in self.data:
            try:

                self.serializer_key = self.get_model_key(key)
                self.serializer = UpdateData.get_serializer(self.serializer_key)
                self.update()
            except Exception as e:
                break

    def update(self):
        if self.serializer_key == 'person_info':
            data = self.data[self.serializer_key]
            serializer = UpdateNamesSerializer(data=data)
            print(serializer.errors)

class DataHandle(UpdateData):
    """
    Auto Handle data fields
    """
    SAVE_TYPES = ('basic', 'person_info')

    @classmethod
    def is_save(cls, data_type):

        if data_type not in cls.SAVE_TYPES:
            return False
        return True

    def __init__(self, request):
        self.request = request
        self.valid_data = {}
        print(request.user.id)
        super().__init__(self.valid_data, request.user.id)

    def check_format(self):
        for data_type in self.request.data:
            if DataHandle.is_save(data_type):
                self.valid_data[data_type] = self.request.data[data_type]
        return super().__init__(self.valid_data, self.request.user.id)



