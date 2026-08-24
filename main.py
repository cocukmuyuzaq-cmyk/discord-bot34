import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
VOUCH_CHANNEL_ID = 1541375320853192774

# Rol ID'leri
ROLE_UNLIMITED = 1539170674986319912
ROLE_1_PER_DAY = 1539170716715585557
ROLE_5_PER_DAY = 1539562464377839656

user_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')

# TÜM HESAPLAR (500+)
steam_accounts = [
    {'user': 'gbjmu99702', 'pass': 'mrt12518', 'game': 'ARK: Survival Ascended'},
    {'user': 'KathleenJools', 'pass': 'Kathleen3527', 'game': "Marvel's Spider-Man Remastered"},
    {'user': 'zfccv56213', 'pass': 'Garethbale11!', 'game': 'Windrose'},
    {'user': 'de_derekch', 'pass': 'OPvj3*all2(4Aqq', 'game': 'BeamNG.drive'},
    {'user': 'ordinaryrhinoceros6358', 'pass': 'a8ef32a3b76effb41!aZ', 'game': 'Stray'},
    {'user': 'ydtdo32097', 'pass': 'PzIf3P1GXw2dEJ', 'game': 'MECCHA CHAMELEON'},
    {'user': 'Cu98721', 'pass': 'Tam0768838298@@', 'game': 'Subnautica 2'},
    {'user': 'flsge218009', 'pass': 'QoYyB497464', 'game': 'Escape from Tarkov'},
    {'user': '23817635', 'pass': 'alfmxldps!11018', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'cmjp18153', 'pass': 'Tedandfr@123', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'perseguini1', 'pass': 'Nazinhomarques@199626', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'GTAVPremiium2', 'pass': 'GtA654347$234', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'msfaraz69', 'pass': 'blj55566', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'phuwadon46', 'pass': '0986375820As', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'taltb554', 'pass': 'uxtz68036IT', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'il2ol8kp5fc0', 'pass': 'Uj5Ih3Jo5Lm7', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'Ha5Lf1Mz1Ce1', 'pass': 'Au4Yt1Xp9Am4', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'beys_7852', 'pass': 'Heel2002', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'CANBAYR5M', 'pass': 'tazemail01', 'game': 'Steam Account'},
    {'user': 'Ntatolo09', 'pass': 'ZXCVBNM.90', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'artinaghaie', 'pass': 'ARTin13921', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'jukk94', 'pass': 'Jucariee94', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'andrettidre', 'pass': 'Percy180', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'zmaloca', 'pass': '123Ponterasa123', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'szqk907', 'pass': 'ajoK1993', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'l3th4lkills', 'pass': 'muhaimin159357', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'tangjie1978643857', 'pass': 'kyiCogfrXj', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'jamespern2', 'pass': 'Bigjump20', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'latte242007za01', 'pass': 'Thanisorn12', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'noahtv098', 'pass': 'NoahTV12', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'uwvehewx', 'pass': 'acqczzkv6Zrt', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'kkcu3909', 'pass': 'PlayGame3.1.26', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'alicgntoraman', 'pass': '200820132008', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'alienlab1', 'pass': 'chelsea201nigga', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'TheJulitoYt', 'pass': '1103505475', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'matheus291207', 'pass': 'johomala4', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'vostm80762', 'pass': 'nixk14958D', 'game': 'Forza Horizon 6'},
    {'user': 'nafeyz227', 'pass': 'Hq123556', 'game': "Assassin's Creed Black Flag"},
    {'user': 'unmqzvh1x6w3', 'pass': 'Scaction@@2026', 'game': 'EA SPORTS FC 26'},
    {'user': 'dgwzg51904', 'pass': 'yusahan7@', 'game': 'The Texas Chain Saw Massacre'},
    {'user': 'toferresident1', 'pass': 'Resident@1122', 'game': 'Resident Evil 4'},
    {'user': 'egoros3p41', 'pass': 'siski33BFa9lCBU7O67483', 'game': 'Resident Evil Requiem'},
    {'user': 'steamok1090115', 'pass': 'steamok36464652', 'game': 'Counter-Strike 2'},
    {'user': 'sugardaddy0076', 'pass': 'SiTatkLCzDqbvyK', 'game': "Tom Clancy's Rainbow Six Siege"},
    {'user': 'tebhy35660', 'pass': 'Okboomer100', 'game': 'EA SPORTS FC 26'},
    {'user': 'tlger38147', 'pass': 'l24p5KCIEsh3', 'game': 'Left 4 Dead 2'},
    {'user': 'tvfnp31656', 'pass': 'pmo090710', 'game': 'Counter-Strike 2'},
    {'user': 'turxw96711', 'pass': 'wofps26557', 'game': 'DayZ'},
    {'user': 'typux41215', 'pass': 'jokk33020N', 'game': 'Counter-Strike 2'},
    {'user': 'udshp23299', 'pass': '4Duen78ksMfvj', 'game': 'EA SPORTS FC 26'},
    {'user': 'uglydeer1764', 'pass': '02c7dbb09d91e9791!aZ', 'game': 'Counter-Strike 2'},
    {'user': 'uqbah000', 'pass': 'uqbahdota', 'game': 'Counter-Strike 2'},
    {'user': 'vdfk61114', 'pass': 'Garethbale11!', 'game': 'Counter-Strike 2'},
    {'user': 'wznyj52220', 'pass': 'oflyq77352', 'game': 'Sons Of The Forest'},
    {'user': 'xlco5u79h', 'pass': 'hdgaming@123', 'game': 'Counter-Strike 2'},
    {'user': 'ycvsw30539', 'pass': 'ogue22576N', 'game': 'Counter-Strike 2'},
    {'user': 'yula69721', 'pass': 'Pj1Zp2Kh9Qb26t', 'game': 'Counter-Strike 2'},
    {'user': 'zestyTacos18415', 'pass': 't03EULbIhCSY', 'game': 'Counter-Strike 2'},
    {'user': 'zwlmi26059', 'pass': 'euxs32929G', 'game': 'Rust'},
    {'user': 'pmo91286', 'pass': 'zxc94877', 'game': 'Counter-Strike 2'},
    {'user': 'papyyafka', 'pass': '71E7UkmGb0MIvq8', 'game': 'Counter-Strike 2'},
    {'user': 'Il0Ys9Tb2Dl8', 'pass': 'Aj5Dz4En4Un7', 'game': 'Counter-Strike 2'},
    {'user': 'MiSide18', 'pass': 'BloodRue-Shop-Mi', 'game': 'Counter-Strike 2'},
    {'user': 'gabrielfrcd6', 'pass': 'SteamJ3#x', 'game': 'Counter-Strike 2'},
    {'user': 'hasyn73382', 'pass': 'jwqe43571W', 'game': 'Counter-Strike 2'},
    {'user': 'mlhao274948', 'pass': 'MyDcT644900', 'game': 'Counter-Strike 2'},
    {'user': 'nohecorni1988', 'pass': 'nv6GJw1AFv1980', 'game': 'Counter-Strike 2'},
    {'user': 'mosapoy10540', 'pass': 'marpanov_free21', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'aboardmoth98933', 'pass': 'Tjddarcy11!', 'game': 'Counter-Strike 2'},
    {'user': 'asser71220114', 'pass': 'Aser12712', 'game': 'Counter-Strike 2'},
    {'user': 'is4ii6ik9kh6', 'pass': 'Kilian1297', 'game': 'ARK: Survival Evolved'},
    {'user': '17261552', 'pass': '91019024', 'game': 'Counter-Strike 2'},
    {'user': 'arimb76284', 'pass': 'mivo63928V', 'game': 'Counter-Strike 2'},
    {'user': 'rzaei96043', 'pass': 'aihz54300L', 'game': 'Counter-Strike 2'},
    {'user': 'piwrbwlq', 'pass': 't1p8w4v6', 'game': 'Counter-Strike 2'},
    {'user': 'abortivelamechamois', 'pass': 'Quietedge24', 'game': 'Counter-Strike 2'},
    {'user': 'widecanid6152', 'pass': 'c3b0bc16d08708211!aZ', 'game': 'Counter-Strike 2'},
    {'user': 'UBER3786', 'pass': 'zRR^h43Rv1rLR', 'game': 'Counter-Strike 2'},
    {'user': 'efficaciousdisturbedmallard', 'pass': 'Thinleaf53', 'game': 'Counter-Strike 2'},
    {'user': 'SolidAbsorbingWhale', 'pass': 'Bravesilk56', 'game': 'Counter-Strike 2'},
    {'user': 'LackadaisicalJoblessFly', 'pass': 'Freshfox93', 'game': 'Counter-Strike 2'},
    {'user': 'xaphan0001', 'pass': '485701793410A', 'game': 'Counter-Strike 2'},
    {'user': 'eaw1sdf', 'pass': 'motherfuck00', 'game': 'Vegas Infinite'},
    {'user': 'kennelxenon52', 'pass': 'sLyOXgh26Ruo', 'game': 'Counter-Strike 2'},
    {'user': 'compa_oscarrr', 'pass': 'VAOLJIdytgap', 'game': 'Crosshair X'},
    {'user': 'dmccl47501', 'pass': 'https://funpay.com/users/11580680/', 'game': 'Resident Evil Requiem'},
    {'user': 'nrbkr70913', 'pass': 'zjjqg11385', 'game': "Marvel's Spider-Man 2"},
    {'user': 'fmfdh768618', 'pass': 'JxOlD541496', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'arenda9126', 'pass': 'Ytrnj275', 'game': 'Forza Horizon 6'},
    {'user': 'Orenda311', 'pass': 'VGJ876gjgift4567FDCFggfgytdsR', 'game': 'God of War Ragnarok'},
    {'user': 'whisperingbarnacle95403', 'pass': 'LavCrewMan03!#', 'game': 'Steam Account'},
    {'user': 'godpris@mail.dk', 'pass': 'Oscar737', 'game': 'Steam Account'},
    {'user': 'demeguszti@freemail.hu', 'pass': 'Pajtikutyus1976', 'game': 'Steam Account'},
    {'user': 'kerike29@freemail.hu', 'pass': 'Nagyati0308', 'game': 'Steam Account'},
    {'user': 'debode@freemail.hu', 'pass': 'machetas00', 'game': 'Steam Account'},
    {'user': 's.jezus@freemail.hu', 'pass': 'jesszuszPQ12', 'game': 'Steam Account'},
    {'user': 'l.davidd@freemail.hu', 'pass': 'Gaborka1221', 'game': 'Steam Account'},
    {'user': 'yyalr@yandex.com', 'pass': 'mxdehzkizqzoondi', 'game': 'Steam Account'},
    {'user': 'joysscott@yandex.com', 'pass': 'jwcsixnjnggerfef', 'game': 'Steam Account'},
    {'user': 'byronmiiller@yandex.ru', 'pass': 'uitubmgaznvynhsc', 'game': 'Steam Account'},
    {'user': 'tiaaburke@yandex.ru', 'pass': 'dvlyovqwbmzoepeo', 'game': 'Steam Account'},
    {'user': 'jorgerose@yandex.com', 'pass': 'qavyznihpjlpwsqs', 'game': 'Steam Account'},
    {'user': 'julia.tolkacheva.666@yandex.ru', 'pass': 'nlidnwazhidnljtk', 'game': 'Steam Account'},
    {'user': 'dev1234543210@yandex.ru', 'pass': 'guvukocnpsmdpqnn', 'game': 'Steam Account'},
    {'user': 'orladean@yandex.ru', 'pass': 'loliimajloubctcm', 'game': 'Steam Account'},
    {'user': 'milapitts@yandex.ru', 'pass': 'jnpipfzfmplxlkok', 'game': 'Steam Account'},
    {'user': 'mamypokopants@yandex.ru', 'pass': 'gorwijvdchyocnkj', 'game': 'Steam Account'},
    {'user': 'carllevy@yandex.ru', 'pass': 'bcsyyhxzudnwgnyz', 'game': 'Steam Account'},
    {'user': 'andreenwil@versatel.nl', 'pass': 'andre2400', 'game': 'Steam Account'},
    {'user': 'luyman2404@movistar.es', 'pass': 'sofalevape', 'game': 'Steam Account'},
    {'user': 'mjcchicoa@movistar.es', 'pass': 'chicoa1202', 'game': 'Steam Account'},
    {'user': 'carllevy@ya.ru', 'pass': 'bcsyyhxzudnwgnyz', 'game': 'Steam Account'},
    {'user': 'herexlaku@ya.ru', 'pass': 'urgkyyweqbytyame', 'game': 'Steam Account'},
    {'user': 'bluipantor@ya.ru', 'pass': 'eheldghouuuwgewo', 'game': 'Steam Account'},
    {'user': 'orladean@ya.ru', 'pass': 'loliimajloubctcm', 'game': 'Steam Account'},
    {'user': 'langgina@ya.ru', 'pass': 'plmpmcfaaqiwkuxr', 'game': 'Steam Account'},
    {'user': 'milapitts@ya.ru', 'pass': 'jnpipfzfmplxlkok', 'game': 'Steam Account'},
    {'user': 'julia.tolkacheva.666@ya.ru', 'pass': 'nlidnwazhidnljtk', 'game': 'Steam Account'},
    {'user': 'jla99002@telefonica.net', 'pass': '!Jla99002', 'game': 'Steam Account'},
    {'user': 'pjferroni@terra.com.br', 'pass': 'Solzinha40@', 'game': 'Steam Account'},
    {'user': 'sensi1@telefonica.net', 'pass': 'chispa', 'game': 'Steam Account'},
    {'user': 'rodrigojosefreitas@bol.com.br', 'pass': '#satierf1981', 'game': 'Steam Account'},
    {'user': '58786917', 'pass': '25925863', 'game': 'Spider-Man: Miles Morales'},
    {'user': 'aegorovsio41', 'pass': 'siski70oO4iI9uU3yY8tT2rR7eE', 'game': 'Resident Evil Requiem'},
    {'user': 'tronghp1234', 'pass': 'Tronghp1232334@', 'game': 'Black Myth Wukong'},
    {'user': 'jvaag15694', 'pass': 'otuu60772Z', 'game': 'Black Myth Wukong'},
    {'user': 'marcuscox2p', 'pass': 'nku6wbav', 'game': 'Black Myth Wukong'},
    {'user': 'hoangnha140203', 'pass': 'hoangnha112233', 'game': 'WWE 2K22'},
    {'user': 'abdullah_kwt21', 'pass': 'Kuwait@22', 'game': 'Steam Account'},
    {'user': '5114599039', 'pass': '0797484206', 'game': 'Steam Account'},
    {'user': 'rostokrrfan1', 'pass': 'alpharacer54', 'game': 'Steam Account'},
    {'user': '2vff29ne', 'pass': 'eoojdisn', 'game': 'Steam Account'},
    {'user': 'Ah5Vc2Oa4Dh0', 'pass': 'Paul100h1996', 'game': 'Steam Account'},
    {'user': 'jhonatan_santos3', 'pass': 'jhonatan952137', 'game': 'Steam Account'},
    {'user': 'bcpc_dyinglight2_0001', 'pass': 'QwYLVG2ptDQkp7jL', 'game': 'Dying Light 2'},
    {'user': '4bdb0e2d', 'pass': 'QAzAS7W6', 'game': 'Dying Light 2: Reloaded Edition'},
    {'user': '3497875991', 'pass': 'ftla1719', 'game': 'Steam Account'},
    {'user': 'hnkl51679', 'pass': '@C2329123d050716', 'game': 'Steam Account'},
    {'user': 'takla_swamijii07', 'pass': 'Tsgame24', 'game': 'Steam Account'},
    {'user': 'dv6fr6st9mq0', 'pass': 'Sn4Ff5Wt6Fc1', 'game': 'Red Dead Redemption 2'},
    {'user': 'cnykqx48s', 'pass': 'Progamer@', 'game': 'Steam Account'},
    {'user': '46mickey46', 'pass': 'Cosmin69', 'game': 'MotoGP 18'},
    {'user': 'c21282', 'pass': 'asdAVXab21Z', 'game': 'Cyberpunk 2077'},
    {'user': 'pbred4', 'pass': 'PrezleyB0', 'game': 'Bendy and the Ink Machine'},
    {'user': 'dhortelio', 'pass': '28*09*04', 'game': 'Construction Simulator'},
    {'user': 'gamerzeygx', 'pass': 't.me\\xoovt', 'game': 'Red Dead Redemption 2'},
    {'user': 'wpjzq59155', 'pass': 'fkwcd30981', 'game': 'RV There Yet?'},
    {'user': 'kdxz65371', 'pass': 'Albert0511*', 'game': 'Grand Theft Auto V Legacy'},
    {'user': 'arenda9121', 'pass': 'Ytrnj274', 'game': 'AAA Games'},
    {'user': 's_danya_s', 'pass': 'Nekt0FPgame', 'game': 'AAA Games'},
    {'user': 'zon_jb', 'pass': 'Tomteland98', 'game': 'Hogwarts Legacy'},
    {'user': 'stefmz', 'pass': 'Panagia91', 'game': 'Call of Duty: Modern Warfare 3'},
    {'user': 'rxt_wrld12', 'pass': 'Bear1010!', 'game': 'F1 22'},
    {'user': 'pbozkziw9', 'pass': 'uiovQ8UF5iwV', 'game': 'F1 25'},
    {'user': 'pablo79911', 'pass': 'F552YFK7K5B9', 'game': 'God of War Ragnarok'},
    {'user': 'zMartins2', 'pass': 'viniciussilvadelima12072008', 'game': 'Grand Theft Auto V Enhanced'},
    {'user': 'correctgoat7561', 'pass': 'c71d741ebd93d7361!aZ', 'game': 'Forza Horizon 4'},
    {'user': 'deancavin', 'pass': 'Wiredpair68', 'game': 'AAA Games'},
    {'user': 'sasuke31053', 'pass': 'lYipMaspH1ra', 'game': 'NARUTO SHIPPUDEN'},
    {'user': '1062218039', 'pass': '1m@@@@@@', 'game': 'Steam Wallet $50'},
    {'user': 'wang2009731', 'pass': 'wang200973', 'game': 'Choo-Choo Charles'},
    {'user': 'avtoritet118', 'pass': 'KSGG8EE76DB9', 'game': 'Call of Duty: Modern Warfare 3'},
    {'user': 'obc7ucchmr', 'pass': 'swambyomar@#$$', 'game': 'ARC Raiders'},
    {'user': 'Blayze100', 'pass': 'sammydog0000', 'game': 'Boris and the Dark Survival'},
    {'user': 'perze50', 'pass': 'Cashman20', 'game': 'Cuphead'},
    {'user': 'rdfv4308', 'pass': 'uuxy0075', 'game': "Sid Meier's Civilization VI"},
    {'user': 'seekkeyeldenring', 'pass': 'SVbviKtWNGIg', 'game': 'ELDEN RING'},
    {'user': 'kl0in5gt5gy8', 'pass': 'SKZT8C9S6G8C', 'game': 'OMORI'},
    {'user': 'jnabf66580', 'pass': 'U11SWgFfmYeAaI', 'game': "Assassin's Creed Shadows"},
    {'user': 'cfni01801', 'pass': 'Mp2Ff7Ex8Pj6', 'game': 'Hunt: Showdown 1896'},
    {'user': 'jordan12707', 'pass': 'Accuakhach123', 'game': 'Left 4 Dead 2'},
    {'user': 'zuakr17055', 'pass': 'BfONDyw2oJp5', 'game': 'WWE 2K25'},
    {'user': 'yczhw46123', 'pass': 'CookieStore1122', 'game': 'Resident Evil Series'},
    {'user': 'njnuf99053', 'pass': 'frxpy52007', 'game': 'Windrose'},
    {'user': 'MatteoC_05', 'pass': 'Franci2007', 'game': 'MotoGP 18'},
    {'user': 'jrmyg57887', 'pass': 'Forever1313', 'game': 'For Honor'},
    {'user': 'madishare11111', 'pass': '79cBeTCpEZjABC_', 'game': 'The Last of Us Part II Remastered'},
    {'user': 'za0an5fh8jr0', 'pass': 'Uz8Hs9Xw4Sq0', 'game': 'Ghostrunner'},
    {'user': 'ogod07', 'pass': 'Mysticlv2', 'game': 'The Last Campfire'},
    {'user': 'RpkR333630', 'pass': 'AzhJ2823', 'game': 'AAA Games'},
    {'user': 'irwhidijar1977', 'pass': '7qllmhp1', 'game': 'The Isle'},
    {'user': 'tomtran81', 'pass': 'WUkong57!asd', 'game': 'Black Myth: Wukong'},
    {'user': 'liujunjie123413', 'pass': 'liujunjie12A', 'game': 'Black Myth: Wukong'},
    {'user': 'lichao5210011', 'pass': 'lichao2948222111qz', 'game': 'Monster Hunter: World'},
    {'user': 'AMAZING123DUDE', 'pass': 'ILuvmom112@', 'game': 'Poppy Playtime'},
    {'user': 'andymystogan', 'pass': 'andy1342', 'game': 'Hitman 2'},
    {'user': 'kruty3', 'pass': 'bossenergi', 'game': 'TOMB RAIDER'},
    {'user': 'anggaprls17', 'pass': 'Enocute05', 'game': 'FIFA 22'},
    {'user': 'megaprang', 'pass': 'EB1234EB!!', 'game': 'Grand Theft Auto IV'},
    {'user': 'mj09uq5kw', 'pass': 'KKg0xvKyzVNs6y', 'game': 'Ready or Not'},
    {'user': 'Cidesplague', 'pass': 'bebedeon1985', 'game': 'HITMAN 2'},
    {'user': 'minymazy', 'pass': '605160253', 'game': 'Mafia II'},
    {'user': 'coranhart', 'pass': 'H9mqE6og31', 'game': 'EA SPORTS FIFA 23'},
    {'user': 'sutencoheadlimesdia', 'pass': 'arczydU1l1skFa', 'game': 'DayZ'},
    {'user': 'cp1cz1qw9ai1', 'pass': 'sunshine1A', 'game': 'Split Fiction'},
    {'user': 'horvb78187', 'pass': '5o1r7muc', 'game': 'Red Dead Redemption 2'},
    {'user': 'antonioralph1972ff', 'pass': '0Oe!brsaxqsn2206', 'game': 'Microsoft Flight Simulator 2024'},
    {'user': 'asymb35468', 'pass': 'HtW5Ar546', 'game': 'EA SPORTS FC 25'},
    {'user': 'schaak77', 'pass': 'hollender07', 'game': 'Tomb Raider'},
    {'user': 'Ei9Cj4Mp7Oe2', 'pass': 'Ib8My5Pw4Jc6', 'game': 'Call of Duty: Modern Warfare III'},
    {'user': 'Vh0Gz5Xs1Qo5', 'pass': 'Ko4Ny7Dt6Sm0', 'game': 'Call of Duty: Modern Warfare III'},
    {'user': 'dzsds89335', 'pass': 'ye988776', 'game': 'Counter-Strike 2'},
]

# ============================================================
# FONKSİYONLAR
# ============================================================

def load_user_data():
    try:
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_user_data(data):
    try:
        os.makedirs(os.path.dirname(user_data_file), exist_ok=True)
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def get_user_role(interaction):
    user_roles = [str(role.id) for role in interaction.user.roles]
    if str(ROLE_UNLIMITED) in user_roles:
        return 'unlimited'
    elif str(ROLE_5_PER_DAY) in user_roles:
        return '5_per_day'
    elif str(ROLE_1_PER_DAY) in user_roles:
        return '1_per_day'
    return 'no_role'

def get_max_limit(role_type):
    if role_type == 'unlimited':
        return float('inf')
    elif role_type == '5_per_day':
        return 5
    elif role_type == '1_per_day':
        return 1
    return 0

def check_user_limit(interaction):
    user_id = str(interaction.user.id)
    role_type = get_user_role(interaction)
    max_limit = get_max_limit(role_type)
    data = load_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in data:
        data[user_id] = {'date': today, 'count': 0, 'last_use': None, 'role': role_type}
    
    if data[user_id].get('role') != role_type:
        data[user_id]['role'] = role_type
        data[user_id]['count'] = 0
    
    if data[user_id]['date'] != today:
        data[user_id]['date'] = today
        data[user_id]['count'] = 0
    
    save_user_data(data)
    return data[user_id], max_limit

def can_use_now(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    role_type = get_user_role(interaction)
    
    if role_type == 'unlimited':
        return True, None
    
    if role_type == '5_per_day':
        if user_id in data and data[user_id].get('last_use'):
            last_use = datetime.fromisoformat(data[user_id]['last_use'])
            time_diff = datetime.now() - last_use
            if time_diff < timedelta(hours=2):
                remaining = timedelta(hours=2) - time_diff
                return False, remaining
        return True, None
    
    return True, None

def update_last_use(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {}
    data[user_id]['last_use'] = datetime.now().isoformat()
    save_user_data(data)

def increment_count(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    if user_id in data:
        data[user_id]['count'] = data[user_id].get('count', 0) + 1
        save_user_data(data)

# ============================================================
# BOT
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

class SteamBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.synced = False

    async def setup_hook(self):
        await self.tree.sync()
        self.synced = True
        print(f'{self.user} olarak giriş yapıldı!')
        print(f'Toplam {len(steam_accounts)} hesap yüklendi!')

bot = SteamBot()
SOON_GIF = 'https://media.tenor.com/LqPwUfj3fwMAAAAM/puppet-red.gif'

async def get_steam_game_image(game_name):
    try:
        search_url = f"https://steamcommunity.com/actions/SearchApps/{game_name.replace(' ', '%20')}"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        app_id = data[0].get('appid')
                        if app_id:
                            return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
    except:
        pass
    return 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2048px-Steam_icon_logo.svg.png'

# ============================================================
# KOMUTLAR
# ============================================================

@bot.tree.command(name='steam', description='Rastgele bir Steam hesabı gösterir.')
async def steam(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    role_type = get_user_role(interaction)
    
    if role_type == 'no_role':
        embed = discord.Embed(
            title='❌ Yetkiniz Yok!',
            description='Bu komutu kullanmak için bir role sahip olmalısınız.\n\n**📋 Roller:**\n• <@&1539170674986319912> - Sınırsız\n• <@&1539562464377839656> - Günde 5 (2 saat aralıkla)\n• <@&1539170716715585557> - Günde 1',
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    user_data, max_limit = check_user_limit(interaction)
    
    if role_type != 'unlimited' and user_data['count'] >= max_limit:
        embed = discord.Embed(
            title='⚠️ Günlük Limit Doldu!',
            description=f'Bugünkü {max_limit} hesap hakkını doldurdun.',
            color=discord.Color.red()
        )
        if role_type == '5_per_day':
            embed.description += '\n\n⏰ Yarın tekrar dene!'
        embed.set_image(url=SOON_GIF)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    if role_type == '5_per_day':
        can_use, remaining = can_use_now(interaction)
        if not can_use:
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            embed = discord.Embed(
                title='⏳ Beklemen Gerekiyor!',
                description=f'2 saat beklemelisin!\n\n**Kalan Süre:** {hours} saat {minutes} dakika',
                color=discord.Color.orange()
            )
            embed.set_image(url=SOON_GIF)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
    
    account = random.choice(steam_accounts)
    increment_count(interaction)
    if role_type == '5_per_day':
        update_last_use(interaction)
    
    user_data, _ = check_user_limit(interaction)
    game_image = await get_steam_game_image(account['game'])
    
    role_info = {
        'unlimited': {'name': '💎 Sınırsız', 'color': discord.Color.gold()},
        '5_per_day': {'name': f'📊 Günde 5 ({user_data["count"]}/5)', 'color': discord.Color.blue()},
        '1_per_day': {'name': f'📊 Günde 1 ({user_data["count"]}/1)', 'color': discord.Color.green()}
    }
    
    embed = discord.Embed(
        title=f'🎮 {account["game"]}',
        description=f'**Kullanıcı Adı:** {account["user"]}\n**Şifre:** {account["pass"]}',
        color=role_info[role_type]['color']
    )
    embed.set_thumbnail(url=game_image)
    embed.add_field(name='👤 Rolün', value=role_info[role_type]['name'], inline=False)
    
    if role_type == '5_per_day':
        remaining = 5 - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
        embed.add_field(name='⏰ Bekleme', value='2 saat aralıkla', inline=True)
    elif role_type == '1_per_day':
        remaining = 1 - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
    elif role_type == 'unlimited':
        embed.add_field(name='♾️ Limit', value='Sınırsız!', inline=True)
    
    embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap • %80 çalışma oranı')
    
    vouch_button = discord.ui.Button(label='✅ Vouch', style=discord.ButtonStyle.success, custom_id='vouch')
    status_button = discord.ui.Button(label='📊 STATUS', style=discord.ButtonStyle.primary, custom_id='status')
    view = discord.ui.View()
    view.add_item(vouch_button)
    view.add_item(status_button)
    
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name='premium', description='Premium abonelik bilgilerini gösterir.')
async def premium(interaction: discord.Interaction):
    embed = discord.Embed(
        title='💎 Premium Abonelik',
        description='**🔜 SOON!**\n\nPremium özellikler yakında geliyor!',
        color=discord.Color.gold()
    )
    embed.add_field(name='✅ Sınırsız Hesap', value='Günlük limit olmadan hesap alabilirsin', inline=False)
    embed.add_field(name='🎁 Özel Hesaplar', value='Sadece premium üyelere özel hesaplar', inline=False)
    embed.add_field(name='⚡ Öncelikli Destek', value='7/24 öncelikli destek hizmeti', inline=False)
    embed.set_image(url=SOON_GIF)
    embed.set_footer(text='🔜 Yakında...')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='myrole', description='Kendi rolünü ve kullanım durumunu gösterir.')
async def myrole(interaction: discord.Interaction):
    role_type = get_user_role(interaction)
    user_data, max_limit = check_user_limit(interaction)
    
    role_names = {
        'unlimited': '💎 Sınırsız (Premium)',
        '5_per_day': f'📊 Günde 5 (Kullanılan: {user_data["count"]}/5)',
        '1_per_day': f'📊 Günde 1 (Kullanılan: {user_data["count"]}/1)',
        'no_role': '❌ Yetkin Yok'
    }
    
    embed = discord.Embed(title='📊 Yetki ve Kullanım Bilgilerin', color=discord.Color.blue())
    embed.add_field(name='👤 Rolün', value=role_names[role_type], inline=False)
    
    if role_type != 'no_role' and role_type != 'unlimited':
        remaining = max_limit - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
    
    if role_type == '5_per_day':
        can_use, remaining = can_use_now(interaction)
        if not can_use:
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            embed.add_field(name='⏳ Bekleme Süresi', value=f'{hours} saat {minutes} dakika', inline=True)
        else:
            embed.add_field(name='✅ Durum', value='Hazır, hesap alabilirsin!', inline=True)
    
    embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap mevcut')
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================================
# BUTON OLAYLARI
# ============================================================

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get('custom_id') == 'vouch':
            try:
                channel = bot.get_channel(VOUCH_CHANNEL_ID)
                if channel:
                    await channel.send(f'✅ Vouch verildi: {interaction.user.mention} tarafından!')
                    await interaction.response.send_message('✅ Vouch kanala gönderildi!', ephemeral=True)
                else:
                    await interaction.response.send_message('❌ Kanal bulunamadı!', ephemeral=True)
            except Exception as e:
                print(f'Hata: {e}')
                await interaction.response.send_message('❌ Bir hata oluştu!', ephemeral=True)
        
        elif interaction.data.get('custom_id') == 'status':
            role_type = get_user_role(interaction)
            user_data, max_limit = check_user_limit(interaction)
            
            role_names = {
                'unlimited': '💎 Sınırsız (Premium)',
                '5_per_day': f'📊 Günde 5 (Kullanılan: {user_data["count"]}/5)',
                '1_per_day': f'📊 Günde 1 (Kullanılan: {user_data["count"]}/1)',
                'no_role': '❌ Yetkin Yok'
            }
            
            embed = discord.Embed(title=f'📊 {interaction.user.name} - Durum Bilgileri', color=discord.Color.blue())
            embed.add_field(name='👤 Rolün', value=role_names[role_type], inline=False)
            
            if role_type == 'unlimited':
                embed.add_field(name='♾️ Limit', value='Sınırsız! 🎉', inline=True)
            elif role_type != 'no_role':
                remaining = max_limit - user_data['count']
                embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
            
            if role_type == '5_per_day':
                can_use, remaining = can_use_now(interaction)
                if not can_use:
                    hours = int(remaining.total_seconds() // 3600)
                    minutes = int((remaining.total_seconds() % 3600) // 60)
                    embed.add_field(name='⏳ Bekleme Süresi', value=f'{hours} saat {minutes} dakika', inline=True)
                    embed.add_field(name='⏰ Durum', value='❌ Beklemede', inline=True)
                else:
                    embed.add_field(name='✅ Durum', value='Hazır! Hesap alabilirsin.', inline=True)
            elif role_type == '1_per_day':
                if user_data['count'] >= 1:
                    embed.add_field(name='⏰ Durum', value='❌ Bugünlük bitti. Yarın dene!', inline=True)
                else:
                    embed.add_field(name='⏰ Durum', value='✅ Hazır! Hesap alabilirsin.', inline=True)
            elif role_type == 'unlimited':
                embed.add_field(name='⏰ Durum', value='✅ Her zaman hazır!', inline=True)
            
            embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap mevcut')
            await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================================
# ADMIN KOMUTLARI
# ============================================================

@bot.tree.command(name='resetall', description='Tüm kullanıcıların limitini sıfırlar (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def reset_all(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    
    data = load_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    for user_id in data:
        data[user_id]['count'] = 0
        data[user_id]['date'] = today
    save_user_data(data)
    await interaction.response.send_message('✅ Tüm kullanıcıların limitleri sıfırlandı!', ephemeral=True)

@bot.tree.command(name='resetuser', description='Bir kullanıcının limitini sıfırlar (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def reset_user(interaction: discord.Interaction, user: discord.User):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    
    user_id = str(user.id)
    data = load_user_data()
    if user_id in data:
        data[user_id]['count'] = 0
        data[user_id]['date'] = datetime.now().strftime('%Y-%m-%d')
        save_user_data(data)
        await interaction.response.send_message(f'✅ {user.mention} limiti sıfırlandı!', ephemeral=True)
    else:
        await interaction.response.send_message(f'❌ {user.mention} için veri bulunamadı!', ephemeral=True)

@bot.tree.command(name='accountcount', description='Toplam hesap sayısını gösterir (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def account_count(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    await interaction.response.send_message(f'📊 Toplam {len(steam_accounts)} Steam hesabı mevcut!', ephemeral=True)

# ============================================================
# BOTU BAŞLAT
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)
