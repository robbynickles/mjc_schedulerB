from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from course_selector.course_selector import course_selector_layout
from calender_visualizer import Calender

top_level_layout = FloatLayout()

course_labels = GridLayout( cols=1, size_hint = (1, .4), pos_hint = {'top':.9} )
courses_selected = []
number_of_courses_selected = 0

inactive_widgets = []
def create_label( dicts, text ):
    global courses_selected
    global number_of_courses_selected
    number_of_courses_selected += 1
    for d in dicts:
        if d['Name'][0] == text:
            courses_selected += [d]
    course_labels.add_widget( Label( text=" ".join([text, courses_selected[-1]['Title'][0]])))

def generate_schedules_button( button ):
    global courses_selected
    global number_of_courses_selected
    global calender
    print '*' * 100
    print courses_selected
    print number_of_courses_selected
    #schedules = generate_schedules(courses_selected, number_of_courses_selected)
    #for course in schedules[0]: calender.add_course( course )
    """
    if len(courses_selected) > 0:
        calender.add_course( courses_selected[0] )
        #print courses_selected[0]['Days'], courses_selected[0]['Times']
    """
    load_calender()

def load_active_widgets():
    global top_level_layout, active_widgets
    top_level_layout.clear_widgets()
    for widg in active_widgets:
        top_level_layout.add_widget(widg)

def load_calender():
    global active_widgets, inactive_widgets, calender
    inactive_widgets, active_widgtets = active_widgets, [calender]
    load_active_widgets()
    
gen_butt = Button( text="Generate Schedules", 
                   size_hint=(1, .1), 
                   pos_hint={'top':.5}, 
                   on_press=generate_schedules_button)

# Wierd part is that create_label is called when a course is selected. 
course_select = course_selector_layout(create_label, top_per=1, x_per=1, y_per=.1)
calender = Calender()

active_widgets = [course_select, gen_butt, course_labels]
load_active_widgets()

runTouchApp(top_level_layout)
