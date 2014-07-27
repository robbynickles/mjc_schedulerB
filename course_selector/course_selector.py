from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from utilkit import find_and_destroy_widget
from scrapekit.session import term_labels, set_term_value, \
    subject_labels, set_subject_value, \
    submit_HTMLform

def course_selector_layout( callout, top_per=0, x_per=1, y_per=1 ):
    layout = GridLayout(cols=3, pos_hint = {'top': top_per}, size_hint=(x_per,y_per))
    
    def make_spinner_with_values( values, text, id, callback ): 
        spinner = Spinner(text=text, values=values, id=id)
        find_and_destroy_widget( layout, id )
        spinner.bind(text=callback)
        layout.add_widget( spinner )
        return spinner

    def term_selected(spinner, text): 
        set_term_value(text)
        
    def dept_selected(spinner, text): 
        set_subject_value(text)
        submit_form()
    
    term_spinner = make_spinner_with_values( term_labels, 'Select a term', 'term', term_selected )
    subject_spinner = make_spinner_with_values( subject_labels, 'Select a department', 'subject', dept_selected )
    
    def wrapper(): 
        wrapper.dictionaries = []

    def course_selected( spinner, text ):
        callout( wrapper.dictionaries, text )
    
    def list_of_dicts_to_widget( dicts ):
        title = lambda d: d['Name'][0]
        return make_spinner_with_values(sorted(set(map(title, dicts))), 'Select a course', 'course', course_selected)

    def submit_form(): 
        wrapper.dictionaries = submit_HTMLform()
        list_of_dicts_to_widget( wrapper.dictionaries )
    return layout

