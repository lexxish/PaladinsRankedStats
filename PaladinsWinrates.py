import sys, os, datetime, pytz, hashlib, requests, json, re, time, gspread, sys, datetime, os, csv, math
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *

devid = '' #INSERT YOUR HIREZ DEV ID
authkey = '' #INSERT YOUR HIREZ AUTH KEY
hour = '-1'

rankindex = ['Qualifying', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Silver', 'Silver', 'Silver', 'Silver', 'Silver', 'Gold', 'Gold', 'Gold', 'Gold', 'Gold', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Master', 'Master', 'All Ranks']

while True:
	t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
	while True:
		try:
			s = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/createsessionJson/{devid}/' + hashlib.md5((f'{devid}createsession{authkey}{t}').encode('utf-8')).hexdigest() + f'/{t}').content)['session_id']
			patch = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/getpatchinfoJson/{devid}/' + hashlib.md5((f'{devid}getpatchinfo{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}').content)['version_string']
			cclasses = enumerate(json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/getchampionsjson/{devid}/' + hashlib.md5((f'{devid}getchampions{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/1').content))
		except Exception as e: 
			print(e)
			continue
		break		
	basedir1 = os.path.dirname(os.path.realpath(__file__))
	cclass = {}
	for ln, lc in cclasses: cclass[lc['Name']] = lc['Roles'].replace('Paladins ', '').replace('Flanker', 'Flank').replace('Front Line', 'Frontline')
	date = datetime.datetime.now()
	if str(datetime.datetime.now().hour) in '0,1,2': date -= datetime.timedelta(days=2)
	else: date -= datetime.timedelta(days=1)
	date = date.date()
	for queue in ['486','428']:
		basedir2 = f'{ basedir1}/{patch} {queue} '
		try: day = open(f'{basedir2}matchcount.json').read()[:8]
		except Exception as e:
			print(e)
			day = '20200109'
		day0 = datetime.datetime(int(day[:4]), int(day[4] + day[5]), int(day[-2:])).date() + datetime.timedelta(days=1)
		while day0 <= date:
			day = str(day0).replace('-', '')
			print(f'{queue} {day}')
			if queue == '486': googlesheetid = '1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg'
			else: googlesheetid = '12TrxqtZbp2G_7p0vJYPOZvpSbCxNHFIFL_d767BTF9g'
			try:
				matchcount = json.loads(open(f'{basedir2}matchcount.json').read()[8:])
				wincount = json.loads(open(f'{basedir2}wincount.json').read()[8:])
			except Exception as e:
				print(e)
				matchcount = {}
				wincount = {}
			try:
				cardmatchcount = json.loads(open(f'{basedir2}cardmatchcount.json').read())
				cardwincount = json.loads(open(f'{basedir2}cardwincount.json').read())
			except Exception as e:
				print(e)
				cardmatchcount = {}
				cardwincount = {}
			
			try:
				itemmatchcount = json.loads(open(f'{basedir2}itemmatchcount.json').read())
				itemwincount = json.loads(open(f'{basedir2}itemwincount.json').read())
			except Exception as e:
				print(e)
				itemmatchcount = {}
				itemwincount = {}
			try:
				compmatchcount = json.loads(open(f'{basedir2}compmatchcount.json').read())
				compwincount = json.loads(open(f'{basedir2}compwincount.json').read())
			except Exception as e:
				print(e)
				compmatchcount = {}
				compwincount = {}
			try:
				enemymatchcount = json.loads(open(f'{basedir2}enemymatchcount.json').read())
				enemywincount = json.loads(open(f'{basedir2}enemywincount.json').read())
			except Exception as e:
				print(e)
				enemymatchcount = {}
				enemywincount = {}
			
			t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
			while True:
				try:
					matches = str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchidsbyqueuejson/{devid}/' + hashlib.md5((f'{devid}getmatchidsbyqueue{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{queue}/{day}/{hour}', timeout=10).content)
				except Exception as e: 
					print(e)
					continue
				break				

			n = len(list(re.finditer('Match":"(.*?)"', matches)))
			x = 0
			m = ''
			for i in re.finditer('Match":"(.*?)"', matches):
				x += 1
				m += f'{i.group(1)},'
				if str(x).endswith('0') or x == n:
					t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
					while True:
						try:
							mdata = requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchdetailsbatchjson/{devid}/' + hashlib.md5((f'{devid}getmatchdetailsbatch{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{m}'[:-1]).content[1:-1].decode('utf-8')
						except Exception as e: 
							print(e)
							continue
						break		
					if '"Reference_Name":null' in str(mdata):
						print(mdata)
						print(m)
						sys.exit()
					m = ''
					print(f'{x}/{n}')
					D = 0
					F = 0
					S = 0
					T = 0
					playernumber = 0
					li = list(mdata.split(',{"Account_Level'))
					for player in li:
						if not player.startswith('{"Account_Level'): player = '{"Account_Level' + player
						player = json.loads(player)
						try: champ = player['Reference_Name'].replace('\\', '')
						except Exception as e:
							print(e)
							print(mdata)
							print('nigga')
							print(player)
							sys.exit()
						if len(li) == 100:
							playernumber += 1
							if player['Item_Purch_6'] == 'Maelstrom': cc = 'Damage'
							elif player['Item_Purch_6'] == 'Catalyst': cc =  'Flank'
							elif player['Item_Purch_6'] == 'Smoke and Dagger': cc =  'Support'
							else: cc = cclass[champ]
							if cc == 'Damage': D += 1
							if cc == 'Flank': F += 1
							if cc == 'Support': S += 1
							if cc == 'Frontline': T += 1
							if playernumber % 5 == 0:
								comp = f'{D}D-{F}F-{S}S-{T}T'
								if comp not in compmatchcount:
									compmatchcount[comp] = 0
									compwincount[comp] = 0
								compmatchcount[comp] += 1
								if player['Win_Status'] == 'Winner': compwincount[comp] += 1
								D = 0
								F = 0
								S = 0
								T = 0
							
							if player['Item_Purch_6'] == '': continue
							batchnumber = playernumber - (playernumber % 10)
							if str(playernumber)[-1:] not in '6,7,8,9,0':
								for lin in [5,6,7,8,9]:
									lin += batchnumber
									enemy = li[lin]
									if not enemy.startswith('{"Account_Level'): enemy = '{"Account_Level' + enemy
									enemy = json.loads(enemy)['Reference_Name']
									champandenemy = f'{champ},{enemy}'
									enemyandchamp = f'{enemy},{champ}'
									if champandenemy not in enemymatchcount:
										enemymatchcount[champandenemy] = 0
										enemywincount[champandenemy] = 0
										enemymatchcount[enemyandchamp] = 0
										enemywincount[enemyandchamp] = 0
									enemymatchcount[champandenemy] += 1
									enemymatchcount[enemyandchamp] += 1
									if player['Win_Status'] == 'Winner': enemywincount[champandenemy] += 1
								
						if player['Item_Purch_6'] == '': continue
						if champ not in cardmatchcount:
							cardmatchcount[champ] = {}
							cardwincount[champ] = {}
						cn = 0
						for card in [player['Item_Purch_1'], player['Item_Purch_2'], player['Item_Purch_3'], player['Item_Purch_4'], player['Item_Purch_5']]:
							cn += 1
							card += ',' + str(player[f'ItemLevel{cn}'])
							if card not in cardmatchcount[champ]:
								cardmatchcount[champ][card] = 0
								cardwincount[champ][card] = 0
							cardmatchcount[champ][card] += 1
							if player['Win_Status'] == 'Winner': cardwincount[champ][card] += 1
						

						for item in [player['Item_Active_1'], player['Item_Active_2'], player['Item_Active_3'], player['Item_Active_4']]:
							if item == '': break
							item = f'{champ},{item}'
							if item not in itemmatchcount:
								itemmatchcount[item] = 0
								itemwincount[item] = 0
							itemmatchcount[item] += 1
							if player['Win_Status'] == 'Winner': itemwincount[item] += 1

						champtalent = f'{champ},' + player['Item_Purch_6'].replace(',' , '').replace('\\', '')
						champrank = f"{champ},{rankindex[player['League_Tier']]}"
						champallranks = f'{champ},All Ranks'
						champmap = f"{champ},{player['Map_Game']}"
						skin = player['Skin'].replace('\\', '').replace(f' {champ}', '')
						champskin = f'{champ},#{skin}'
						rank = rankindex[player['League_Tier']]
						if champtalent not in matchcount: matchcount[champtalent] = 0
						if champtalent not in wincount: wincount[champtalent] = 0
						if champrank not in matchcount: matchcount[champrank] = 0
						if champrank not in wincount: wincount[champrank] = 0
						if champallranks not in matchcount: matchcount[champallranks] = 0
						if champallranks not in wincount: wincount[champallranks] = 0
						if champmap not in matchcount: matchcount[champmap] = 0
						if champmap not in wincount: wincount[champmap] = 0
						if champskin not in matchcount: matchcount[champskin] = 0
						if champskin not in wincount: wincount[champskin] = 0
						if rank not in matchcount: matchcount[rank] = 0
						if rank not in wincount: wincount[rank] = 0
						matchcount[champtalent] += 1
						matchcount[champrank] += 1
						matchcount[champallranks] += 1
						matchcount[champmap] += 1
						matchcount[champskin] += 1
						matchcount[rank] += 1
						if rank == 'Diamond' or rank == 'Master':
							rankchamptalent = f'Diamond+,{champtalent}'
							if rankchamptalent not in matchcount: matchcount[rankchamptalent] = 0
							if rankchamptalent not in wincount: wincount[rankchamptalent] = 0
							matchcount[rankchamptalent] += 1
						if player['Win_Status'] == 'Winner':
							wincount[champtalent] += 1
							wincount[champrank] += 1
							wincount[champallranks] += 1
							wincount[champmap] += 1
							wincount[champskin] += 1
							wincount[rank] += 1
							if rank == 'Diamond' or rank == 'Master': wincount[rankchamptalent] += 1
								
			while True:
				try:
					print(str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getdatausedjson/{devid}/' + hashlib.md5((f'{devid}getdataused{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}').content))
				except Exception as e: 
					print(e)
					continue
				break							

			gcs = [gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(f'{basedir1}/sheetsapikey1.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])), gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(f'{basedir1}/sheetsapikey2.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])), gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(f'{basedir1}/sheetsapikey3.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']))]
		
			gcn = 0
			gc = gcs[gcn]
			
			if hour == '-1':
				open(f'{basedir2}matchcount.json', 'w').write(str(day) +  json.dumps(matchcount))
				open(f'{basedir2}wincount.json', 'w').write(str(day) +  json.dumps(wincount))
				open(f'{basedir1}/paladinswinrates backup/{patch} {queue} matchcount {day} {hour}.json', 'w').write(str(day) +  json.dumps(matchcount))
				open(f'{basedir1}/paladinswinrates backup/{patch} {queue} wincount {day} {hour}.json', 'w').write(str(day) +  json.dumps(wincount))
				open(f'{basedir2}cardmatchcount.json', 'w').write( json.dumps(cardmatchcount))
				open(f'{basedir2}cardwincount.json', 'w').write( json.dumps(cardwincount))
				open(f'{basedir2}itemmatchcount.json', 'w').write( json.dumps(itemmatchcount))
				open(f'{basedir2}itemwincount.json', 'w').write( json.dumps(itemwincount))
				open(f'{basedir2}compmatchcount.json', 'w').write( json.dumps(compmatchcount))
				open(f'{basedir2}compwincount.json', 'w').write( json.dumps(compwincount))
				open(f'{basedir2}enemymatchcount.json', 'w').write( json.dumps(enemymatchcount))
				open(f'{basedir2}enemywincount.json', 'w').write( json.dumps(enemywincount))

			cardWRs = []
			for champ, cards in cardmatchcount.items():
				for card, cardmatchcount in cards.items():
					D = cardwincount[champ][card] / cardmatchcount
					E = cardmatchcount
					H = D*E
					I = E-H
					J = 2.5758293035489
					C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
					C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
					D = str(D*100).split('.')[0] + '%'
					if len(D) == 2: D = f'0{D}'
					C1 = str(C1*100).split('.')[0] + '%'
					if len(C1) == 2: C1 = f'0{C1}'
					C2 = str(C2*100).split('.')[0] + '%'
					if len(C2) == 2: C2 = f'0{C2}'
					cardWRs.append((f'{champ},{card}', D, E, C1, C2))
					
			cardWRs.sort(key=lambda x:(x[0].split(',')[2], x[3], x[1], x[2]), reverse=True)
			cardWRs.sort(key=lambda x:(x[0].split(',')[0]))
			open(f'{basedir2}cardWRs.csv', 'w').write(str(f'Champion,Card,Card Level,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(cardWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]))
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Card',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}cardWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			itemWRs = []
			for item, itemmatchcount in itemmatchcount.items():
				D = itemwincount[item] / itemmatchcount
				E = itemmatchcount
				H = D*E
				I = E-H
				J = 2.5758293035489
				C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
				C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
				D = str(D*100).split('.')[0] + '%'
				if len(D) == 2: D = f'0{D}'
				C1 = str(C1*100).split('.')[0] + '%'
				if len(C1) == 2: C1 = f'0{C1}'
				C2 = str(C2*100).split('.')[0] + '%'
				if len(C2) == 2: C2 = f'0{C2}'
				itemWRs.append((item, D, E, C1, C2))
			
			itemWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			itemWRs.sort(key=lambda x:(x[0].split(',')[0]))
			open(f'{basedir2}itemWRs.csv', 'w').write(str(f'Champion,Item,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(itemWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]))
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Item',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}itemWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			compWRs = []
			for comp, compmatchcount in compmatchcount.items():
				D = compwincount[comp] / compmatchcount
				E = compmatchcount
				H = D*E
				I = E-H
				J = 2.5758293035489
				C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
				C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
				D = str(D*100).split('.')[0] + '%'
				if len(D) == 2: D = f'0{D}'
				C1 = str(C1*100).split('.')[0] + '%'
				if len(C1) == 2: C1 = f'0{C1}'
				C2 = str(C2*100).split('.')[0] + '%'
				if len(C2) == 2: C2 = f'0{C2}'
				compWRs.append((comp, D, E, C1, C2))
				
			compWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			open(f'{basedir2}compWRs.csv', 'w').write(str(f'Composition,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(compWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]))
						
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Composition',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}compWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			enemyWRs = []
			for item, enemymatchcount in enemymatchcount.items():
				D = enemywincount[item] / enemymatchcount
				E = enemymatchcount
				H = D*E
				I = E-H
				J = 2.5758293035489
				C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
				C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
				D = str(D*100).split('.')[0] + '%'
				if len(D) == 2: D = f'0{D}'
				C1 = str(C1*100).split('.')[0] + '%'
				if len(C1) == 2: C1 = f'0{C1}'
				C2 = str(C2*100).split('.')[0] + '%'
				if len(C2) == 2: C2 = f'0{C2}'
				enemyWRs.append((item, D, E, C1, C2))
			
			enemyWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			enemyWRs.sort(key=lambda x:(x[0].split(',')[0]))
			open(f'{basedir2}enemyWRs.csv', 'w').write(str(f'1st Champion,2nd Champion,v{patch} 1st Champion Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(enemyWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]))
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Enemy Champion',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}enemyWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
				
			WRs = []
			for i1, i2 in matchcount.items():
				winrate = str(wincount[i1] / i2)[:4]
				WRs.append((i1, float(winrate), i2))
			talentwinrates = []
			diamondpustalentwinrates = []
			rankwinrates = []
			mapwinrates = []
			skinwinrates = []
			avgrankwinrates = {}

			for i in WRs:
				D = i[1]
				E = i[2]
				H = D*E
				I = E-H
				J = 2.5758293035489
				C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
				C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
				D = str(i[1]*100).split('.')[0] + '%'
				C1 = str(C1*100).split('.')[0] + '%'
				C2 = str(C2*100).split('.')[0] + '%'
				if '#' in i[0]: skinwinrates.append((i[0].replace('#', ''), D, E, C1, C2))
				elif 'Ranked' in i[0]: mapwinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}'.replace('Ranked ',''), D, E, C1, C2)) 
				elif any(f',{r}' in i[0] for r in rankindex): rankwinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}', D, E, C1, C2))
				elif any(r == i[0] for r in rankindex): avgrankwinrates[i[0]] = str(i[1]*100).split('.')[0] + '%'
				elif i[0].startswith('Diamond+,'):
					i0 = i[0].replace('Diamond+,', '')
					i0 = cclass[i0.split(',')[0]] + f',{i0}'
					i0 = i0.replace("Support,Grohk,Maelstrom", "Damage,Grohk,Maelstrom").replace("Support,Pip,Catalyst", "Flank,Pip,Catalyst").replace("Flank,Skye,Smoke and Dagger", "Support,Skye,Smoke and Dagger")
					diamondpustalentwinrates.append((i0, D, E, C1, C2))
				else:
					i0 = cclass[i[0].split(',')[0]] + f',{i[0]}'
					i0 = i0.replace("Support,Grohk,Maelstrom", "Damage,Grohk,Maelstrom").replace("Support,Pip,Catalyst", "Flank,Pip,Catalyst").replace("Flank,Skye,Smoke and Dagger", "Support,Skye,Smoke and Dagger")
					talentwinrates.append((i0, D, E, C1, C2))
			
			skinwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			skinwinrates.sort(key=lambda x: x[0].split(',')[0])
			mapwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			mapwinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
			rankwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			rankwinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
			talentwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			talentwinrates.sort(key=lambda x: x[0].split(',')[0])
			diamondpustalentwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
			diamondpustalentwinrates.sort(key=lambda x: x[0].split(',')[0])

			open(f'{basedir2}skinWRs.csv', 'w').write(f'Champion,Skin,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(skinwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Skin',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}skinWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			open(f'{basedir2}mapWRs.csv', 'w').write(f'Class,Champion,Map,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(mapwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Map',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}mapWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break

			rankwinrates = str(rankwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]
			rankwinrates = rankwinrates.replace('All Ranks', 'All Ranks: 50%')
			for r in ['Qualifying', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master']: rankwinrates = rankwinrates.replace(r, f'{r}: ' +	avgrankwinrates[r])
			open(f'{basedir2}rankWRs.csv', 'w').write(f'Class,Champion,Player Rank: its average winrate,v{patch} Champion Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + rankwinrates)
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
					'By Player Rank',
					params={'valueInputOption': 'USER_ENTERED'},
					body={'values': list(csv.reader(open(f'{basedir2}rankWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break

			open(f'{basedir2}talentWRs.csv', 'w').write(f'Source Code: https://github.com/Aevann1/PaladinsWinrates\nClass,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(talentwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])
		
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
						'By Talent (All Ranks)',
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': list(csv.reader(open(f'{basedir2}talentWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
			while True:
				try:
					format_cell_range(sheet, 'A1:E2', cellFormat(textFormat=textFormat(bold=True)))
					format_cell_range(sheet, f'B3:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
					continue
				break


			sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
			n = 1
			cnames = ''
			for val in gc.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)').col_values(2):
				while True:
					try:
						if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
						if val not in cnames:
							format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
							cnames += f'{val},'
					except Exception as e:
						print(json.loads(str(e))['error']['message'])
						gcn += 1
						gc = gcs[gcn]
						sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
						continue
					n += 1
					break
			
			diawr = (wincount['Diamond'] + wincount['Master']) / (matchcount['Diamond'] + matchcount['Master'])
			diawr = str(diawr*100).split('.')[0] + '%'
			open(f'{basedir2}diamondplustalentWRs.csv', 'w').write(f'Average Diamond+ winrate for all champions and talents: {diawr}\nClass,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(diamondpustalentwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])
			
			sheet = gc.open_by_key(googlesheetid)
			while True:
				try:
					sheet.values_update(
					'By Talent (Diamond+)',
					params={'valueInputOption': 'USER_ENTERED'},
					body={'values': list(csv.reader(open(f'{basedir2}diamondplustalentWRs.csv')))})
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid)
					continue
				break
			
			sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
			while True:
				try:
					format_cell_range(sheet, 'A1:E2', cellFormat(textFormat=textFormat(bold=True)))
					format_cell_range(sheet, f'B3:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
				except Exception as e:
					print(json.loads(str(e))['error']['message'])
					gcn += 1
					gc = gcs[gcn]
					sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
					continue
				break
			
			sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
			n = 1
			cnames = ''
			for val in gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)').col_values(2):
				while True:
					try:
						if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
						if val not in cnames:
							format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
							cnames += f'{val},'
					except Exception as e:
						print(json.loads(str(e))['error']['message'])
						gcn += 1
						gc = gcs[gcn]
						sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
						continue
					n += 1
					break
			day0 += datetime.timedelta(days=1)
	wakeuptime = datetime.datetime.now().replace(hour=3, minute=0)
	if str(datetime.datetime.now().hour) not in '0,1,2': wakeuptime += datetime.timedelta(days=1)
	print(f'Sleeping until {wakeuptime}')
	time.sleep((wakeuptime - datetime.datetime.now()).total_seconds())
