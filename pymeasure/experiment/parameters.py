#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2015 Colin Jermain, Graham Rowlands
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


class Parameter(object):
    """ Encapsulates the information for an experiment parameter
    with information about the name, and unit if supplied.

    :var value: The value of the parameter

    :param name: A short description of the parameter (no colons allowed)
    :param default: The default value
    :param ui_class: A Qt class to use for the UI of this parameter
    """

    def __init__(self, name, default=None, ui_class=None):
        self.name = name
        self._value = default
        self.default = default
        self.ui_class = None

    @property
    def value(self):
        if self.is_set():
            return self._value
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        self._value = value

    def is_set(self):
        """ Returns True if the Parameter value is set
        """
        return self._value is not None

    def __str__(self):
        return str(self._value) if self.is_set() else ''

    def __repr__(self):
        return "<%s(name=%s,value=%s,default=%s)>" % (
            self.__class__.__name__, self.name, self._value, self.default)


class IntegerParameter(Parameter):
    """ :class:`.Parameter` sub-class that uses the integer type to
    store the value.

    :var value: The integer value of the parameter

    :param name: A short description of the parameter (no colons allowed)
    :param units: The units of measure for the parameter
    :param default: The default integer value
    """

    def __init__(self, name, unit=None, minimum=-1e9, maximum=1e9, **kwargs):
        super(IntegerParameter, self).__init__(name, **kwargs)
        self.unit = unit
        self.minimum = minimum
        self.maximum = maximum

    @property
    def value(self):
        if self.is_set():
            return int(self._value)
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("IntegerParameter given non-integer value of "
                             "type '%s'" % type(value))
        if value < self.minimum:
            raise ValueError("IntegerParameter value is below the minimum")
        elif value > self.maximum:
            raise ValueError("IntegerParameter value is above the maximum")
        else:
            self._value = value

    def __str__(self):
        if not self.is_set():
            return ''
        result = "%d" % self._value
        if self.unit:
            result += " %s" % self.unit
        return result

    def __repr__(self):
        return "<%s(name=%s,value=%s,unit=%s,default=%s)>" % (
            self.__class__.__name__, self.name, self._value, self.unit, self.default)


class BooleanParameter(Parameter):
    """ :class:`.Parameter` sub-class that uses the boolean type to
    store the value.

    :var value: The boolean value of the parameter

    :param name: A short description of the parameter (no colons allowed)
    :param default: The default boolean value
    """

    @property
    def value(self):
        if self.is_set():
            return self._value
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        try:
            self._value = bool(value)
        except ValueError:
            raise ValueError("BooleanParameter given non-boolean value of "
                             "type '%s'" % type(value))


class FloatParameter(Parameter):
    """ :class:`.Parameter` sub-class that uses the floating point
    type to store the value.

    :var value: The floating point value of the parameter

    :param name: A short description of the parameter (no colons allowed)
    :param unit: The unit of measure for the parameter
    :param default: The default floating point value
    """

    def __init__(self, name, unit=None, minimum=-1e9, maximum=1e9, **kwargs):
        super(FloatParameter, self).__init__(name, **kwargs)
        self.unit = unit
        self.minimum = minimum
        self.maximum = maximum

    @property
    def value(self):
        if self.is_set():
            return float(self._value)
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError("FloatParameter given non-float value of "
                             "type '%s'" % type(value))
        if value < self.minimum:
            raise ValueError("FloatParameter value is below the minimum")
        elif value > self.maximum:
            raise ValueError("FloatParameter value is above the maximum")
        else:
            self._value = value

    def __str__(self):
        if not self.is_set():
            return ''
        result = "%g" % self._value
        if self.unit:
            result += " %s" % self.unit
        return result

    def __repr__(self):
        return "<%s(name=%s,value=%s,unit=%s,default=%s)>" % (
            self.__class__.__name__, self.name, self._value, self.unit, self.default)


class VectorParameter(Parameter):
    """ :class:`.Parameter` sub-class that stores the value in a
    vector format.

    :var value: The value of the parameter as a list of floating point numbers

    :param name: A short description of the parameter (no colons allowed)
    :param length: The integer dimensions of the vector
    :param unit: The units of the vector
    :param default: The default value
    """
    def __init__(self, name, length=3, unit=None, default=None):
        # TODO: Update VectorParameter with new methods
        self.name = name
        self._value = default
        self.unit = unit
        self.default = default
        self._length = length

    @property
    def value(self):
        if self.is_set():
            return [float(ve) for ve in self._value]
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        # Strip initial and final brackets
        if isinstance(value, basestring):
            if (value[0] != '[') or (value[-1] != ']'):
                raise ValueError("VectorParameter must be passed a vector"
                                 " denoted by square brackets if initializing"
                                 " by string.")
            raw_list = value[1:-1].split(",")
        elif isinstance(value, (list, tuple)):
            raw_list = value
        else:
            raise ValueError("VectorParameter given undesired value of "
                             "type '%s'" % type(value))
        if len(raw_list) != self._length:
            raise ValueError("VectorParameter given value of length "
                             "%d instead of %d" % (len(raw_list), self._length))
        try:
            self._value = [float(ve) for ve in raw_list]

        except ValueError:
            raise ValueError("VectorParameter given input '%s' that could "
                             "not be converted to floats." % str(value))

    def __repr__(self):
        if not self.is_set():
            raise ValueError("Parameter value is not set")
        result = "<VectorParameter(name='%s'" % self.name
        result += ",value=%s" % "".join(repr(self.value).split())
        if self.unit:
            result += ",unit='%s'" % self.unit
        return result + ")>"

    def __str__(self):
        """If we eliminate spaces within the list __repr__ then the
        csv parser will interpret it as a single value."""
        if not self.is_set():
            raise ValueError("Parameter value is not set")
        result = ""
        result += "%s" % "".join(repr(self.value).split())
        if self.unit:
            result += " %s" % self.unit
        return result


class ListParameter(Parameter):
    """ :class:`.Parameter` sub-class that stores the value as a list.

    :param name: A short description of the parameter (no colons allowed)
    :param choices: An explicit list of choices, which is disregarded if None
    :param unit: The units of the vector
    :param default: The default value

    """

    def __init__(self, name, choices=None, unit=None, default=None):
        # TODO: Update ListParameter with new methods
        self.name = name
        self._value = default
        self.unit = unit
        self.default = default
        self._choices = choices

    @property
    def value(self):
        if self.is_set():
            return self._value
        else:
            raise ValueError("Parameter value is not set")

    @value.setter
    def value(self, value):
        if self._choices is not None and value in self._choices:
            self._value = value
        else:
            raise ValueError("Invalid choice for parameter. "
                             "Must be one of %s" % str(self._choices))

    def is_set(self):
        return self._value is not None
