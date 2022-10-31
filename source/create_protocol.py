import sys
import datetime

# Argument from main.py
TRIAL_NUM = int(sys.argv[1])
PATH_OUT = sys.argv[2]

BODY_RED_VOL   = float(sys.argv[3])
BODY_GREEN_VOL = float(sys.argv[4])
BODY_BLUE_VOL  = float(sys.argv[5])

# create new protocol
f = open(f'{PATH_OUT}/slime_protocol_{TRIAL_NUM}.py', 'w')
code = f'''from opentrons import protocol_api

metadata = {{
	'protocolName': 'Slime protocol trial {TRIAL_NUM} for geekten 2022',
	'author': 'Kensuke Tozuka <knsktzkml@gmail.com>',
	'apiLevel': '2.0'
}}

def run(protocol: protocol_api.ProtocolContext):

	# Labware
	tiprack   = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
	container = protocol.load_labware('eppendorf_6_well_cell_culture_plate_5000ul', '2')
	plate	  = protocol.load_labware('violamo_96_wellplate_370ul', '3')
	pipette   = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

	# Ink wells
	ink = {{
        'red'  :'A1', 
        'green':'A2',
        'blue' :'A3',
		'mouth':'B2',
		'eye'  :'B3',
    }}

    # Target wells
	wells = {{

		'body': [
			'A6', 'A7',
			'B5', 'B6', 'B7', 'B8',
			'C4', 'C6', 'C7', 'C9',
			'D3', 'D10',
			'E2', 'E3', 'E4', 'E6', 'E7', 'E9', 'E10', 'E11',
			'F2', 'F3', 'F5', 'F6', 'F7', 'F8', 'F10', 'F11',
			'G3', 'G4', 'G9', 'G10',
			'H4', 'H5', 'H6', 'H7', 'H8', 'H9'
        ],

		'mouth': [
			'F4', 'F9',
			'G5', 'G6', 'G7', 'G8'
        ],

		'eye': ['D5', 'D8'],
    }}

	# 
	body_parts = ('body',) # 'mouth', 'eye',
	aspirate_vol = 300.0

	# Color info
	class Color():
		def __init__(self, name, body): #mouth, eye):
			self.name  = name
			self.body  = body
			#self.mouth = mouth
			#self.eye   = eye

	red   = Color('red',   {BODY_RED_VOL})
	green = Color('green', {BODY_GREEN_VOL})
	blue  = Color('blue',  {BODY_BLUE_VOL})

	# Functions
	def dispence_template(part): # mouth & eyes

		template_vol = 150

		pipette.pick_up_tip()
		pipette.aspirate( aspirate_vol, container[ink[part]] )
		residual_vol = 300

		for well in wells[part]:
			if residual_vol < template_vol:

				pipette.aspirate( aspirate_vol, container[ink[part]] )
				residual_vol = 300
					
			pipette.dispense( template_vol, plate[well] )
			residual_vol -= template_vol
		
		pipette.drop_tip()

	def dispence_1st(color): # 1st dispence process

		pipette.pick_up_tip()
		pipette.aspirate( aspirate_vol, container[ink[color.name]] )
		residual_vol = 300

		dispence_vol_info = (color.body,) # color.mouth, color.eye)

		for part , dispence_vol in zip(body_parts, dispence_vol_info):

			if dispence_vol == 0:
				continue
			
			for well in wells[part]:

				if residual_vol < dispence_vol:

					pipette.aspirate( aspirate_vol - residual_vol, container[ink[color.name]] )
					residual_vol = 300
				
				pipette.dispense( dispence_vol, plate[well] )
				residual_vol -= dispence_vol

		pipette.drop_tip()

	def dispence_2nd_and_3rd(color): # 2nd and 3rd dispence process

		dispence_vol_info = (color.body,) # color.mouth, color.eye)

		for part , dispence_vol in zip(body_parts, dispence_vol_info):

			if dispence_vol == 0:
				continue

			pipette.pick_up_tip()
			pipette.aspirate( aspirate_vol, container[ink[color.name]] )
			residual_vol = 300

			for well in wells[part]:

				if residual_vol < dispence_vol:
					pipette.drop_tip()
					pipette.pick_up_tip()
					pipette.aspirate( aspirate_vol - residual_vol, container[ink[color.name]] )
					residual_vol = 300
				
				pipette.dispense( dispence_vol, plate[well] )
				residual_vol -= dispence_vol

			pipette.drop_tip()

	def mixer():

		for part in body_parts:
			pipette.pick_up_tip()

			for well in wells[part]:
				pipette.mix(1, 80, plate[well])

			pipette.drop_tip()


	### Dispence run

	# mouth
	dispence_template('mouth')
	dispence_template('eye')

	# trial
	if red.body == max(red.body, green.body, blue.body):
		dispence_1st(red)
		dispence_2nd_and_3rd(green)
		dispence_2nd_and_3rd(blue)
		mixer()
	
	elif green.body == max(red.body, green.body, blue.body):
		dispence_1st(green)
		dispence_2nd_and_3rd(red)
		dispence_2nd_and_3rd(blue)
		mixer()

	else:
		dispence_1st(blue)
		dispence_2nd_and_3rd(red)
		dispence_2nd_and_3rd(green)
		mixer()
'''

f.write(code)
f.close()