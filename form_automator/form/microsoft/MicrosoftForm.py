from time import sleep
from typing import Any, List

from ...Source import Source
from ...MicrosoftSource import MicrosoftSource
from ..Form import Form
from ..FormComponent import FormComponent
from .components.Select import Select
from .components.Radio import Radio
from .components.Text import Text
from .components.DatePicker import DatePicker
from .MicrosoftFormComponent import MicrosoftFormComponent
from .MicrosoftFormComponentType import MicrosoftFormComponentType


class MicrosoftForm(Form):
    def __init__(self, url: str = "", source: 'Source' = None, components: List['FormComponent'] = [], email_confirmation: bool = True) -> None:
        super(MicrosoftForm, self).__init__(url, components=components,
                                            source=source)
        self.url = url
        self.email_confirmation = email_confirmation
        if components == []:
            self.login_if_needed()
            self.components = self.find_components()

    def login_if_needed(self):
        if isinstance(self.source, MicrosoftSource):
            self.source.driver.get(self.url)

            sleep(4)

            if self.source.needs_login():
                self.source.login()

            sleep(4)

    def fill_in(self, responses: List[Any]):
        for i, c in enumerate(self.components):
            c.fill_in(response=responses[i])
        if self.email_confirmation:
            self.__select_email_check_box()

        sleep(2)

        self.send()

    def send(self):
        if len(self.components) >= 1:
            submit_btn = self.source.driver.find_element_by_xpath(
                './/*[contains(@class, "__submit-button__")]')
            submit_btn.click()

    def __select_email_check_box(self):
        try:
            container = self.source.driver.find_element_by_class_name(
                'office-form-email-receipt-checkbox')
            check_box = container.find_element_by_css_selector(
                'input[type=checkbox]')
            check_box.click()
        except:
            pass

    def find_components(self) -> List['FormComponent']:

        form_container = self.source.driver.find_element_by_class_name(
            'office-form-question-body')
        childs = form_container.find_elements_by_xpath(
            './/*[contains(@class, "__question__")]')
        components = []
        for c in childs:
            type = MicrosoftFormComponent.get_type(c)

            if type == MicrosoftFormComponentType.SELECT:
                components.append(Select(web_element=c))
            elif type == MicrosoftFormComponentType.DATE_PICKER:
                components.append(DatePicker(web_element=c))
            elif type == MicrosoftFormComponentType.TEXT:
                components.append(Text(web_element=c))
            elif type == MicrosoftFormComponentType.RADIO:
                components.append(Radio(web_element=c))

        return components
