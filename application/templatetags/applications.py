from django import template
from django.template.defaultfilters import stringfilter
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name = 'application_string')
def get_information(application):
    value = json.loads(application.data)
    application_html = f'''
                        <div class="row">
                            <div class="container pb-2">
                                <div class="row g-2">
                                    <div class="col-6">
                                        <h5>Type: </h5> {value['type']}
                                    </div>
                                    <div class="col-6">
                                        <h5>Academic year: </h5> {value['academic_year']}
                                    </div>
                                    <div class="col-6">
                                        <h5>Country: </h5> {value['country']}
                                      </div>
                                    <div class="col-6">
                                        <h5>University: </h5> {value['university']}
                                    </div>
                                    <div class="col-6">
                                        <h5>Desired speciality: </h5> {value['desired_specialty']}
                                    </div>
                                    <div class="col-6"></div><div class="col-6"></div>
                                    
                                </div>
                            </div>
                            
                        </div>
                        '''
    return mark_safe(application_html)

@register.filter(name = 'status_str')
def status_str(flag):
    if flag == True:
        return 'Заполнен'
    return 'Не заполнен'

@register.filter(name = 'get_file_name')
def get_file_name(file):
    return file.split('/')[3]