#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import random

def voc_input():
	print "Please input the vocabuaries."
	voc = raw_input()
	vocs = []
	while voc != "":
		vocs.append(voc)
		voc = raw_input()
	return vocs

def content_find(page, start_mark, end_mark, where_start):
	start = page.text.find(start_mark, where_start)
	end = page.text.find(end_mark, start+1)
	content = page.text[start + len(start_mark): end]
	return content

def voc_lookup(vocs):
	if vocs != []:
		sleep_last_check = 0
		for voc in vocs:
			page = requests.get("http://dict.dreye.com/ews/%s--01--.html" % voc)
			voc_output = voc + "\n"
			if str(page)[11:14] == "200":
				def_exist = page.text.find(voc)
				if def_exist < 418 : #確認有單字在'</title>'前，此單字存在
					def_para_content = ""
					def_head_mark = '<div class="t_red">'
					def_mark = '<div  class="default" ondblclick="cross_seek(950)" onmouseup="cross_seeka(950)" >'
					def_head_posi = page.text.find(def_head_mark)
					while def_head_posi != -1:
						def_head_content = content_find(page,def_head_mark,'<',def_head_posi)
						def_para_content = def_head_content + "\n"
						def_content_position = page.text.find(def_mark,def_head_posi + 1)
						next_head_posi = page.text.find(def_head_mark, def_head_posi + 1) #next head
						if next_head_posi != -1 :
							while def_content_position < next_head_posi : #test whether it is over the next head
								def_content = content_find(page,def_mark,'<',def_content_position)
								def_para_content = def_para_content + '  ' + def_content + '\n'
								def_content_position = page.text.find(def_mark,def_content_position + 1)
						else:
							botton_mark = u'\u5faa\u73af\u5b57\u5178'
							botton_mark_posi = page.text.find(botton_mark)
							while def_content_position < botton_mark_posi and def_content_position != -1:
								def_content = content_find(page,def_mark,'<',def_content_position)
								def_para_content = def_para_content + "  " + def_content + '\n'
								def_content_position = page.text.find(def_mark,def_content_position + 1)
						voc_output = voc_output + def_para_content
						def_para_content = ""
						def_head_posi = next_head_posi
					print voc_output
				else: #此單字不存在
					voc_output = voc_output + u'\u672a\u67e5\u8a62\u5230\u76f8\u95dc\u55ae\u5b57\u3002' + '\n'
					print voc_output
			else:
				print "Sorry, request is failed."
				break
			sleep_last_check = sleep_last_check + 1
			if sleep_last_check < len(vocs):
				time.sleep(random.randint(0,10))
			else:
				pass
	else:
		pass

def again(again_ask):
	if again_ask.lower() == 'y' or again_ask.lower() == "yes":
		voc_lookup(voc_input())
		print "Again? (Y/N)"
		again_ask = raw_input()
		again(again_ask)
	elif again_ask.lower() == 'n' or again_ask.lower() == "no":
		print "Thank you for using.Please input any letter."
		stop_Q = raw_input()
	else:
		print "Don't trick me!Get out my way!"
		final_chance = raw_input()
		final_chance = final_chance.lower()
		chance_start = final_chance.find('sorry')
		if final_chance[chance_start: chance_start + 5] == "sorry":
			print "..."
			voc_lookup(voc_input())
			print "Again? (Y/N)"
			again_ask = raw_input()
			again(again_ask)
		else:
			pass


print "Welcome to Dr.eye BookCrawler v1.1!\n"
print "Please input the vocabuaries you want to look up."
print "If you'd like to stop,please enter to let me know."
voc = raw_input()
vocs = []
while voc != "":
	vocs.append(voc)
	voc = raw_input()
voc_lookup(vocs)
print "Again? (Y/N)"
again_ask = raw_input()
again(again_ask)