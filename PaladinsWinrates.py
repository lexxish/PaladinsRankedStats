import sys, os, datetime, pytz, hashlib, requests, json, re, time, gspread, sys, datetime, os, csv, math
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *

devid = '' #INSERT YOUR HIREZ DEV ID
authkey = '' #INSERT YOUR HIREZ AUTH KEY
hour = '-1'

while True:
	for queue in ['486','428']:
		if queue == '486': googlesheetid = '1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg'
		else: googlesheetid = '12TrxqtZbp2G_7p0vJYPOZvpSbCxNHFIFL_d767BTF9g'
		matchcount = {}
		wincount = {}
		date = datetime.datetime.now()
		if str(datetime.datetime.now().hour) in '0,1,2': date -= datetime.timedelta(days=2)
		else: date -= datetime.timedelta(days=1)
		month = str(date.month)
		if len(month) == 1: month = f'0{month}'
		day = str(date.year) + month + str(date.day)
		t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
		s = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/createsessionJson/{devid}/' + hashlib.md5((f'{devid}createsession{authkey}{t}').encode('utf-8')).hexdigest() + f'/{t}').content)['session_id']
		patch = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/getpatchinfoJson/{devid}/' + hashlib.md5((f'{devid}getpatchinfo{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}').content)['version_string']
		basedir0 = os.path.dirname(os.path.realpath(__file__))
		basedir = basedir0 + f'/{patch} {queue} '

		rankindex = ['Qualifying', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Silver', 'Silver', 'Silver', 'Silver', 'Silver', 'Gold', 'Gold', 'Gold', 'Gold', 'Gold', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Master', 'Master']
		cclass = {"Androxus": "Flank", "Ash": "Frontline", "Atlas": "Frontline", "Barik": "Frontline", "Bomb King": "Damage", "Buck": "Flank", "Cassie": "Damage", "Dredge": "Damage", "Drogoz": "Damage", "Evie": "Flank", "Fernando": "Frontline", "Furia": "Support", "Grohk": "Support", "Grover": "Support", "Imani": "Damage", "Inara": "Frontline", "Io": "Support", "Jenos": "Support", "Khan": "Frontline", "Kinessa": "Damage", "Koga": "Flank", "Lex": "Flank", "Lian": "Damage", "Maeve": "Flank", "Makoa": "Frontline", "Mal'Damba": "Support", "Moji": "Flank", "Pip": "Support", "Raum": "Frontline", "Ruckus": "Frontline", "Seris": "Support", "Sha Lin": "Damage", "Skye": "Flank", "Strix": "Damage", "Talus": "Flank", "Terminus": "Frontline", "Tiberius": "Damage", "Torvald": "Frontline", "Tyra": "Damage", "Viktor": "Damage", "Vivian": "Damage", "Willo": "Damage", "Ying": "Support", "Zhin": "Flank"}

		try: open(f'{basedir}Matchcount.json').read()
		except:
			open(f'{basedir}Matchcount.json', 'w').write('00000000' + '{}')
			open(f'{basedir}Wincount.json', 'w').write('00000000' + '{}')
		if open(f'{basedir}Matchcount.json').read().startswith(str(day)): print('Day already compiled.')
		else:
			matches = str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchidsbyqueuejson/{devid}/' + hashlib.md5((f'{devid}getmatchidsbyqueue{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{queue}/{day}/{hour}').content)

			n = len(list(re.finditer('Match":"(.*?)"', matches)))
			x = 0
			m = ''
			for i in re.finditer('Match":"(.*?)"', matches):
				try:
					x += 1
					m += f'{i.group(1)},'
					if str(x).endswith('0') or x == n:
						t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
						mdata = requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchdetailsbatchjson/{devid}/' + hashlib.md5((f'{devid}getmatchdetailsbatch{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{m}'[:-1]).content[1:-1].decode('utf-8')
						if 'Reference_Name' not in mdata:
							print(mdata)
							print('Exitting')
							sys.exit()
						print(f'{x}/{n}')
						for player in mdata.split(',{"Account_Level'):
							if not player.startswith('{"Account_Level'): player = '{"Account_Level' + player
							player = json.loads(player)
							if player['Item_Purch_6'] == '': continue
							champtalent = player['Reference_Name'] + ',' + player['Item_Purch_6'].replace(',' , '')
							champtalent = champtalent.replace('\\', '')
							champrank = player['Reference_Name'] + ',' + rankindex[player['League_Tier']]
							champrank = champrank.replace('\\', '')
							champmap = player['Reference_Name'] + ',' + player['Map_Game']
							champmap = champmap.replace('\\', '')
							skin = player['Skin']
							if ' ' + player['Reference_Name'] in skin: skin = skin.replace(' ' + player['Reference_Name'] , '')
							champskin = player['Reference_Name'] + ',#' + skin
							champskin = champskin.replace('\\', '')
							rank = rankindex[player['League_Tier']]
							if champtalent not in str(matchcount): matchcount[champtalent] = 0
							if champtalent not in str(wincount): wincount[champtalent] = 0
							if champrank not in str(matchcount): matchcount[champrank] = 0
							if champrank not in str(wincount): wincount[champrank] = 0
							if champmap not in str(matchcount): matchcount[champmap] = 0
							if champmap not in str(wincount): wincount[champmap] = 0
							if champskin not in str(matchcount): matchcount[champskin] = 0
							if champskin not in str(wincount): wincount[champskin] = 0
							if f"'{rank}'" not in str(matchcount): matchcount[rank] = 0
							if f"'{rank}'" not in str(wincount): wincount[rank] = 0
							matchcount[champtalent] += 1
							matchcount[champrank] += 1
							matchcount[champmap] += 1
							matchcount[champskin] += 1
							matchcount[rank] += 1
							if rank == 'Diamond' or rank == 'Master':
								rankchamptalent = f'Diamond+,{champtalent}'
								if rankchamptalent not in str(matchcount): matchcount[rankchamptalent] = 0
								if rankchamptalent not in str(wincount): wincount[rankchamptalent] = 0
								matchcount[rankchamptalent] += 1
							if player['Win_Status'] == 'Winner':
								wincount[champtalent] += 1
								wincount[champrank] += 1
								wincount[champmap] += 1
								wincount[champskin] += 1
								wincount[rank] += 1
								if rank == 'Diamond' or rank == 'Master': wincount[rankchamptalent] += 1
							elif player['Win_Status'] != 'Loser':
								Print('Match in progress')
								sys.exit()
							m = ''
							mn = 0
				except Exception as e:
					print(f'Error: {e}')
					time.sleep(60)
					open(f'{basedir}Errors.txt', 'a').write(f'Error: {e}\n')
			print(str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getdatausedjson/{devid}/' + hashlib.md5((f'{devid}getdataused{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}').content))

		matchcountfile = json.loads(open(f'{basedir}Matchcount.json').read()[8:])
		for k in matchcountfile: 
				if k in matchcount: matchcount[k] += matchcountfile[k] 
				else: matchcount[k] = matchcountfile[k]
				 
		wincountfile = json.loads(open(f'{basedir}Wincount.json').read()[8:])
		for k in wincountfile: 
				if k in wincount: wincount[k] += wincountfile[k] 
				else: wincount[k] = wincountfile[k]

		if hour == '-1':
			open(f'{basedir}Matchcount.json', 'w').write(str(day) + json.dumps(matchcount))
			open(f'{basedir}Wincount.json', 'w').write(str(day) + json.dumps(wincount))
			open(f'{basedir0}/PaladinsWinrates Backup/{patch} {queue} Matchcount {day} {hour}.json', 'w').write(str(day) + json.dumps(matchcount))
			open(f'{basedir0}/PaladinsWinrates Backup/{patch} {queue} Wincount {day} {hour}.json', 'w').write(str(day) + json.dumps(wincount))

		WR = []
		for i1, i2 in matchcount.items():
			winrate = str(wincount[i1] / i2)[:4]
			WR.append((i1, float(winrate), i2))
		TalentWinrates = []
		DiamondPlusTalentWinrates = []
		RankWinrates = []
		MapWinrates = []
		SkinWinrates = []
		AvgRankWinrates = {}

		for i in WR:
			D = i[1]
			E = i[2]
			H = D*E
			I = E-H
			J = 2.5758293035489
			C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
			C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
			E = str(E)
			D = str(i[1]*100).split('.')[0] + '%'
			C1 = str(C1*100).split('.')[0] + '%'
			C2 = str(C2*100).split('.')[0] + '%'
			if '#' in i[0]: SkinWinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}'.replace('#', ''), D, E, C1, C2))
			elif 'Ranked' in i[0]: MapWinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}'.replace('Ranked ',''), D, E, C1, C2)) 
			elif any(f',{r}' in i[0] for r in rankindex): RankWinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}', D, E, C1, C2))
			elif any(r == i[0] for r in rankindex): AvgRankWinrates[i[0]] = str(i[1]*100).split('.')[0] + '%'
			elif i[0].startswith('Diamond+,'):
				i0 = i[0].replace('Diamond+,', '')
				i0 = cclass[i0.split(',')[0]] + f',{i0}'
				i0 = i0.replace("Support,Grohk,Maelstrom", "Damage,Grohk,Maelstrom").replace("Support,Pip,Catalyst", "Flank,Pip,Catalyst").replace("Flank,Skye,Smoke and Dagger", "Support,Skye,Smoke and Dagger")
				DiamondPlusTalentWinrates.append((i0, D, E, C1, C2))
			else:
				i0 = cclass[i[0].split(',')[0]] + f',{i[0]}'
				i0 = i0.replace("Support,Grohk,Maelstrom", "Damage,Grohk,Maelstrom").replace("Support,Pip,Catalyst", "Flank,Pip,Catalyst").replace("Flank,Skye,Smoke and Dagger", "Support,Skye,Smoke and Dagger")
				TalentWinrates.append((i0, D, E, C1, C2))

		SkinWinrates.sort(key=lambda x:x[2], reverse=True)
		SkinWinrates.sort(key=lambda x:x[1], reverse=True)
		SkinWinrates.sort(key=lambda x:x[3], reverse=True)
		SkinWinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
		MapWinrates.sort(key=lambda x:x[2], reverse=True)
		MapWinrates.sort(key=lambda x:x[1], reverse=True)
		MapWinrates.sort(key=lambda x:x[3], reverse=True)
		MapWinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
		RankWinrates.sort(key=lambda x:x[2], reverse=True)
		RankWinrates.sort(key=lambda x:x[1], reverse=True)
		RankWinrates.sort(key=lambda x:x[3], reverse=True)
		RankWinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
		TalentWinrates.sort(key=lambda x:x[2], reverse=True)
		TalentWinrates.sort(key=lambda x:x[1], reverse=True)
		TalentWinrates.sort(key=lambda x:x[3], reverse=True)
		TalentWinrates.sort(key=lambda x: x[0].split(',')[0])
		DiamondPlusTalentWinrates.sort(key=lambda x:x[2], reverse=True)
		DiamondPlusTalentWinrates.sort(key=lambda x:x[1], reverse=True)
		DiamondPlusTalentWinrates.sort(key=lambda x:x[3], reverse=True)
		DiamondPlusTalentWinrates.sort(key=lambda x: x[0].split(',')[0])

		gc1 = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(f'{basedir0}/sheetsapikey1.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']))		
		gc2 = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(f'{basedir0}/sheetsapikey2.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']))

		open(f'{basedir}SkinWinrates.csv', 'w').write(f'Class,Champion,Skin,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(SkinWinrates).replace('"' , "'").replace("'), ('" , "\n").replace("', '" , ",").replace("')", "")[3:-1])
		
		sheet = gc1.open_by_key(googlesheetid)
		while True:
			try:
				sheet.values_update(
					'By Skin',
					params={'valueInputOption': 'USER_ENTERED'},
					body={'values': list(csv.reader(open(f'{basedir}SkinWinrates.csv')))})
			except:
				sheet = gc2.open_by_key(googlesheetid)
				continue
			break
		
		open(f'{basedir}MapWinrates.csv', 'w').write(f'Class,Champion,Map,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(MapWinrates).replace('"' , "'").replace("'), ('" , "\n").replace("', '" , ",").replace("')", "")[3:-1])
		
		sheet = gc1.open_by_key(googlesheetid)
		while True:
			try:
				sheet.values_update(
					'By Map',
					params={'valueInputOption': 'USER_ENTERED'},
					body={'values': list(csv.reader(open(f'{basedir}MapWinrates.csv')))})
			except:
				sheet = gc2.open_by_key(googlesheetid)
				continue
			break

		RankWinrates = str(RankWinrates).replace('"' , "'").replace("'), ('" , "\n").replace("', '" , ",").replace("')", "")[3:-1]
		for r in ['Qualifying', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master']: RankWinrates = RankWinrates.replace(r, f'{r}: ' +	AvgRankWinrates[r])
		open(f'{basedir}RankWinrates.csv', 'w').write(f'Class,Champion,Player Rank: its average winrate,v{patch} Champion Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + RankWinrates)
		
		sheet = gc1.open_by_key(googlesheetid)
		while True:
			try:
				sheet.values_update(
				'By Player Rank',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir}RankWinrates.csv')))})
			except:
				sheet = gc2.open_by_key(googlesheetid)
				continue
			break

		open(f'{basedir}TalentWinrates.csv', 'w').write(f'Class,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(TalentWinrates).replace('"' , "'").replace("'), ('" , "\n").replace("', '" , ",").replace("')", "")[3:-1])
		
		sheet = gc1.open_by_key(googlesheetid)
		while True:
			try:
				sheet.values_update(
					'By Talent (All Ranks)',
					params={'valueInputOption': 'USER_ENTERED'},
					body={'values': list(csv.reader(open(f'{basedir}TalentWinrates.csv')))})
			except:
				sheet = gc2.open_by_key(googlesheetid)
				continue
			break
		
		sheet = gc1.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
		while True:
			try:
				format_cell_range(sheet, 'A1:E1', cellFormat(textFormat=textFormat(bold=True)))
				format_cell_range(sheet, f'B2:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
			except:
				sheet = gc2.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
				continue
			break			
			
		n = 1
		cnames = ''
		for val in gc2.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)').col_values(2):
			while True:
				try:
					if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
					if val not in cnames:
						format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
						cnames += f'{val},'
				except:
					sheet = gc2.open_by_key(googlesheetid).worksheet('By Talent (All Ranks)')
					continue
				n += 1
				break
		
		diawr = (wincount['Diamond'] + wincount['Master']) / (matchcount['Diamond'] + matchcount['Master'])
		diawr = str(diawr*100).split('.')[0] + '%'
		open(f'{basedir}Diamond+TalentWinrates.csv', 'w').write(f'Average Diamond+ winrate for all champions and talents: {diawr},,,,,,\nClass,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval (-),Confidence Interval (+)\n' + str(DiamondPlusTalentWinrates).replace('"' , "'").replace("'), ('" , "\n").replace("', '" , ",").replace("')", "")[3:-1])
		
		sheet = gc1.open_by_key(googlesheetid)
		while True:
			try:
				sheet.values_update(
				'By Talent (Diamond+)',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir}Diamond+TalentWinrates.csv')))})
			except:
				sheet = gc2.open_by_key(googlesheetid)
				continue
			break
		
		sheet = gc1.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
		while True:
			try:
				format_cell_range(sheet, 'A1:E2', cellFormat(textFormat=textFormat(bold=True)))
				format_cell_range(sheet, f'B3:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
			except:
				sheet = gc2.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
				continue
			break
		
		n = 1
		cnames = ''
		for val in gc2.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)').col_values(2):
			while True:
				try:
					if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
					if val not in cnames:
						format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
						cnames += f'{val},'
				except:
					sheet = gc2.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
					continue
				n += 1
				break

	wakeuptime = datetime.datetime.now().replace(hour=3, minute=0)
	if str(datetime.datetime.now().hour) not in '0,1,2': wakeuptime += datetime.timedelta(days=1)
	print(f'Sleeping until {wakeuptime}')
	time.sleep((wakeuptime - datetime.datetime.now()).total_seconds())
