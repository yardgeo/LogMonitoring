from dataclasses import dataclass, field, fields

from exceptions import LogLineParsingException


@dataclass
class LogLineDto:
    """
    A class to represent a line of logs
    """
    remotehost: str
    rfc931: str
    authuser: str
    date: float
    request: str
    status: float
    bytes: float

    # post inits
    http_method: str = field(init=False)
    web_site_section: str = field(init=False)

    def __post_init__(self):
        """
        Post init logic.
        Include fields validation and post init fields creation
        """
        # validate types
        for self_field in fields(self):
            # check if field was init
            if not self_field.init:
                continue

            # get cur value
            field_value = getattr(self, self_field.name)

            # check if none
            if field_value is None:
                raise LogLineParsingException(
                    f"{self_field.name} attribute is missing"
                )

            # check type
            if not isinstance(field_value, self_field.type):
                raise LogLineParsingException(
                    f"Invalid type for {self_field.name}"
                )

        # parse request variables
        try:
            self.http_method = self.request.split()[0]
            self.web_site_section = self.request.split()[1].split("/")[1]
        except IndexError:
            raise LogLineParsingException("Invalid request format")

    @property
    def unix_time(self) -> int:
        """
        Return log timestamp in unix format
        :return: log unix time
        :rtype: int
        """
        return int(self.date)

    @property
    def status_code(self) -> int:
        """
        return request status code
        :return: status code
        :rtype: int
        """
        return int(self.status)
