import os
from pprint import pprint

from pygame import Rect

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label
import colors


class NowPlaying(Scene):
    def __init__(self, sonos):
        Scene.__init__(self)                        
        self.sonos = sonos
        self.sonos.current_zone = 'TV Room'     
        print("Current Zone: {}".format(self.sonos.current_zone))
        # Listen for all changes to the current zone   
        self.sonos.listen_for_zone_changes(self.zone_state_changed)

        self.firstLoad = True
        self.background_color = colors.NAVY   

        # Track Title   
        self.track_label = Label(Rect(20,226,280,30),"",36, colors.WHITE)             
        self.add_child(self.track_label)    
        # Artist
        self.artist_label = Label(Rect(20,266,280,20),"",24, colors.GRAY)             
        self.add_child(self.artist_label)
        # Album
        self.album_label = Label(Rect(20,291,280,20),"",24, colors.GRAY)             
        self.add_child(self.album_label)

        ##### Play Button #####
        play_track_img = Image('play_track','play_track.png')
        #Center bottom positioning
        self.play_button = Button(Rect(130,330,60,60),image=play_track_img)
        #Touch Handler
        self.play_button.on_tapped.connect(self.play)
        self.add_child(self.play_button)

        ##### Pause Button #####
        pause_track_img = Image('pause_track','pause_track.png')
        #Center bottom positioning
        self.pause_button = Button(Rect(130,330,60,60),image=pause_track_img)
        #Hide to start
        self.pause_button.hidden = True        
        #Touch Handler
        self.pause_button.on_tapped.connect(self.pause)
        self.add_child(self.pause_button)

        ##### Previous Button #####
        previous_track_img = Image('previous_track','previous_track.png')
        previous_track_disabled_img = Image('previous_track_disabled','previous_track_disabled.png')        
        self.previous_button = Button(Rect(65,340,40,40),image=previous_track_img, disabled_image=previous_track_disabled_img)
        #Touch Handler
        self.previous_button.on_tapped.connect(self.previous)
        self.add_child(self.previous_button)

        ##### Next Button #####
        next_track_img = Image('next_track','next_track.png')
        next_track_disabled_img = Image('next_track_disabled','next_track_disabled.png')        
        self.next_button = Button(Rect(215,340,40,40),image=next_track_img,disabled_image=next_track_disabled_img)                
        #Touch Handler
        self.next_button.on_tapped.connect(self.next)
        self.add_child(self.next_button)

        self.layout()


        # Hide all children to start, will unhide when we load everything
        for child in self.children:
            pass
            child.hidden = True

    
    def show_ui(self):
        for child in self.children:
            child.hidden = False

    def play(self, button):        
        # Technically, we don't need to call this here, but it helps with 
        # the UI responsiveness, so we don't need to wait for the listener to respond
        self.update_play_pause('PLAYING')
        self.sonos.play()

    def pause(self, button):
        self.update_play_pause('PAUSED_PLAYBACK')
        self.sonos.pause()
    
    def next(self, button):
        self.sonos.next()

    def previous(self, button):
        self.sonos.previous()

    def update_play_pause(self, state):        
        if state == 'PLAYING':
            self.play_button.hidden = True
            self.pause_button.hidden = False
        elif state == 'PAUSED_PLAYBACK' or state == 'STOPPED':
            self.play_button.hidden = False
            self.pause_button.hidden = True

    def update_available_actions(self, actions):
        print(actions)
        self.next_button.enabled = 'Next' in actions
        self.previous_button.enabled = 'Previous' in actions

    def update_track_info(self,track):
        print(track['duration'])
        print(track['position'])
        print(track['album_art'])
        self.track_label.text = track['title']
        self.artist_label.text = track['artist']
        self.album_label.text = track['album']

    def zone_state_changed(self, data):
        '''Callback function that is called every time the zone state changes ex. new track, play, pause, volume change, etc.'''        
        # print("")
        # pprint(data)
        # print("")

        if self.firstLoad:  
            self.show_ui()
            self.firstLoad = False            

        if 'current_transport_actions' in data: self.update_available_actions(data['current_transport_actions'].split(', '))
        if 'transport_state' in data: self.update_play_pause(data['transport_state'])
        if 'track' in data: self.update_track_info(data['track'])

        
       