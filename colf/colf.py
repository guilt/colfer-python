from .colf_base import TypeDeriveValueMixin, DictMixIn
from .colf_marshall import ColferMarshallerMixin
from .colf_unmarshall import ColferUnmarshallerMixin


class Colfer(DictMixIn, TypeDeriveValueMixin, ColferMarshallerMixin, ColferUnmarshallerMixin):

    def __delitem__(self, name):
        raise NotImplementedError('Del {} is unimplementable.'.format(name))

    def validateKnownAttribute(self, name, variableType, value, variableSubType = None):
        if value is not None:
            if not self.isType(value, variableType):
                raise AttributeError('Attribute {} is of type {}. Cannot be assigned to {}'.format(name, variableType, value))
            if variableSubType and self.isList(value):
                for valueSub in value:
                    if not self.isType(valueSub, variableSubType):
                        raise AttributeError('Attribute {} is of type {}:{}. Cannot be assigned to {}'.format(name, variableType, variableSubType, valueSub))
        else:
            value = self.getValue(variableType)
        return value

    def declareAttribute(self, name, variableType, value=None, variableSubType=None):
        if name is None or variableType is None or type(variableType) is not str:
            raise AttributeError('Must declare a valid attribute and type')
        if name in dir(self):
            raise AttributeError('Cannot declare attribute {} again'.format(name))
        self.setKnownAttribute(name, variableType, value, variableSubType)
