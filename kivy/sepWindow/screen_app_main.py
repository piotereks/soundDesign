# Program to Show how to create a switch
# import kivy module
import kivy
	
# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App
	
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# Builder is used when .kv file is
# to be used in .py file
from kivy.lang import Builder

# The screen manager is a widget
# dedicated to managing multiple screens for your application.
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)


# Create a class for all screens in which you can include
# helpful methods specific to that screen
class ScreenOne(Screen):
	pass

class ScreenTwo(Screen):
	pass

class ScreenThree(Screen):
	pass

class ScreenFour(Screen):
	pass

class ScreenFive(Screen):
	pass


# The ScreenManager controls moving between screens
# You can change the transitions accordingly
# screen_manager = ScreenManager(transition = RiseInTransition())

# # Add the screens to the manager and then supply a name
# # that is used to switch screens
# screen_manager.add_widget(ScreenOne(name ="screen_one"))
# screen_manager.add_widget(ScreenTwo(name ="screen_two"))
# screen_manager.add_widget(ScreenThree(name ="screen_three"))
# screen_manager.add_widget(ScreenFour(name ="screen_four"))
# screen_manager.add_widget(ScreenFive(name ="screen_five"))

# Create the App class
# class ScreenApp(App):
# 	def build(self):
# 		return ScreenManager

class ScreenApp(App):
    pass

# run the app
# sample_app = ScreenApp()
# sample_app.run()
ScreenApp.run()