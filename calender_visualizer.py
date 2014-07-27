from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from kivy.graphics import Color, Bezier, Line, Rectangle

from random import randint

half = [ i +':00'for i in ['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']] 
curry_me = lambda s: lambda i: i + s 
am = curry_me('A')
pm = curry_me('P')
times = map(am, half) + map(pm, half) 

relevant_times = times[6:23]
days = dict( zip( ['M','T','W','TH','F'], range(5) ) )

def split_time(hour):
    colon = hour.find(':')
    return hour[:colon] + ":00" + hour[-1], int(hour[colon+1:-1])

def set_origin(ox, oy):
    def give_point(day,hour):
        hour, min = split_time(hour)
        x_gap, y_gap = 100, 20
        ret = [days[day]*x_gap + ox, relevant_times.index(hour)*y_gap + (y_gap*(min/60.0)) + oy]
        return ret
    return give_point

def extract_times( time_string ):
    spl = time_string.split()
    if len(spl) >= 3:
        return spl[0], spl[2]
    else:
        return '06:00A', '06:00A'
give_widg_point = set_origin(-200, -200)
give_canv_point = set_origin(190, 96)

class Calender(FloatLayout):

    def __init__(self, *args, **kwargs):
        super(Calender, self).__init__(*args, **kwargs)
        self.d = 10
        self.current_point = None
        self.build_border()

    def build_border( self ):
        for d in days.keys():
            pos = give_widg_point(d,'06:00A')
            pos[1] -= 40
            self.add_widget(Label(text=d, pos=pos))
        for t in relevant_times:
            pos = give_widg_point('M',t)
            pos[0] -= 100
            self.add_widget(Label(text=t, pos=pos))

    def add_block( self, day_list, start, end, color, text ):
        for day in day_list:
            if day in days.keys():
                # A course may have non-traditional days and times that don't
                # need calender representation. 
                p1, p2 = give_canv_point(day, start), give_canv_point(day, end)
                canvas_holder = FloatLayout(pos=(0,0), size=(1000, 100))
                r,g,b = color
                with canvas_holder.canvas:
                    #Color(r,g,b)
                    Color(123, 23, 89)
                    Rectangle(size=(100,p2[1]-p1[1]), pos=p1)
                self.add_widget(canvas_holder)

    def add_course( self, course_dict ):
        color = randint(0,255), randint(0,255), randint(0,255)
        time_data = zip(course_dict['Days'], course_dict['Times'], course_dict['Type'])
        for d_list, t, ty in time_data:
            start, end = extract_times(t)
            self.add_block( d_list, start, end, color, ty )


course_dict = {'Name': ['MART-175'], 'Title': ['Color Photography', '08/25/14-12/13/14', 'Material Fee = $45.00'], 'Section': ['2672'], 'Days': ['T', 'TH', 'T', 'TH'], 'Times': ['01:15P - 02:40P', '02:40P - 04:05P', '02:40P - 04:05P', '01:15P - 02:40P'], 'Avail': ['Open'], 'Location': ['MADM 208, West', 'MADM 208, West'
, 'MADM 208, West', 'MADM 208, West'], 'Units': ['3'], 'Instructor': ['Staff03'], 'Type': ['LEC', 'LAB', 'LAB', 'LAB'], 'Important Notes': [''], 'Max/': ['20/11']}

if __name__ == '__main__':

    class Main(App):

        def build(self):
            c = Calender()
            c.add_course( course_dict )
            return c

    main = Main()
    main.run()

