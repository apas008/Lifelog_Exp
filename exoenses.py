# ColorMixer

'''A simple RGB color mixer with three sliders. The selected color can be copied to the clipboard as an HTML hex string.'''

import ui
import clipboard,shortcuts,webbrowser,os
from random import random
from console import hud_alert
from vika import Vika
from objc_util import *
vika = Vika("usk6Zl1kR8gjvDpTpOYjfep")
# 通过 datasheetId 来指定要从哪张维格表操作数据。
dst = vika.datasheet("dstT6RuWUeMVfJ6Tji", field_key="name")

num = 1
amount = ''
def slider_action(sender):
	# Get the root view:
	v = sender.superview
	#print(v)
	# Get the sliders:
	r = v['slider2'].value
	if v['segmentedcontrol2'].symbol < 0: #expenses
		v['slider2'].amount = int(r*(v['segmentedcontrol2'].symbol)*150)
	else:# investment
		if r >= 0.5:
			v['slider2'].amount = int((r-0.5)*1000)
		else:
			v['slider2'].amount = int((0.5-r)*(-1)*1000)

	
	#print(r)
	# Create the new color from the slider values:
	#v['view1'].background_color = '#a40000'
	v['label2'].text = ' ¥'+str(v['slider2'].amount)+'.00'

#	v['label2'].text = '#%.02X%.02X%.02X' % (2,2,int(r*255))
def seg_action(sender):
	v = sender.superview
	print(v['segmentedcontrol2'].selected_index)
	if v['segmentedcontrol2'].selected_index ==0: #expenses
		sender.superview['label3'].text=''
		v['segmentedcontrol2'].symbol = -1
		v['label11'].text = '🧋Drinks'
		v['label12'].text = '🍟Meals'
		v.bg_color = '#fff4f0'
		v.add_subview(ui.load_view('exoenses')['segmentedcontrol1'])
		#v['segmentedcontrol1'].alpha = 1
	elif v['segmentedcontrol2'].selected_index ==1: #revenue
		sender.superview['label3'].text=''
		v['segmentedcontrol2'].symbol = 1
		v['label11'].text = '📈Stock'
		v['label12'].text = '📉Fund'
		v.bg_color = '#ffe071'
		#v['segmentedcontrol1'].alpha = 0
		v.remove_subview(v['segmentedcontrol1'])
def seg1_action (sender):
	v = sender.superview
	if sender.selected_index == 0:#支付宝
		
		v['button1'].bg_color='#276bea'
		v['button1'].title='🏧Submit'
	else:
		v['button1'].bg_color='#36f478'
		v['button1'].title='💹Submit'
		v['button1'].eborder_color='#36f478'
		hud_alert(sender.segments[1])
		
def btn_action(sender):
	v = sender.superview
	category = sender.superview['label3'].text
	amount = int(sender.superview['slider2'].amount)
	if v['segmentedcontrol2'].symbol < 0: #expenses
		item = str(v['segmentedcontrol1'].segments[v['segmentedcontrol1'].selected_index])
	else:
		item = 'Investment'
	record = dst.records.create({"选项": item,"备注":category,"金额":amount})
	

	if v['segmentedcontrol2'].symbol < 0:
		if str(v['segmentedcontrol1'].segments[v['segmentedcontrol1'].selected_index]) == 'Alipay':
			if v['switch3'].value == True:
				shortcuts.open_shortcuts_app(name='AlipayScan')
			else:
				shortcuts.open_shortcuts_app(name='AlipayPay')
		elif str(v['segmentedcontrol1'].segments[v['segmentedcontrol1'].selected_index]) == 'Wechat':
		# la = ObjCClass('LSApplicationWorkspace').alloc()
		# Bid = 'com.tencent.xin'
		# la.openApplicationWithBundleID_(Bid)
			webbrowser.open('weixin://dl/')
		#shortcuts.open_shortcuts_app(name='AlipayScan')
	else:
		hud_alert(category)
	

def switch_action(sender):
	v = sender.superview
	idx = v['segmentedcontrol2'].selected_index
	if sender.value == True:
		#category = ''
		sender.superview['label3'].text = str(sender.text[idx])
		
#slider_action(v['slider2'])
v = ui.load_view('exoenses')

slider_action(v['slider2'])
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present()
	#v.title_color = 'yellow'
	#v.text = 'ttt'
