from PIL import Image
import csv
import re
import subprocess
import sys

# Input:
#     deckListPath: デッキリスト(MO形式, .txt)へのパス
# Output:
#     [0-9]{3}.png: プロキシ画像(各ファイルにつきカード9枚)

# 引数チェック: ちょうど1つの引数をとらなければエラー終了
if(len(sys.argv) != 2):
	print('usage: deck2png.py deckListPath')
	exit(1)

deckListPath = sys.argv[1]

# 入力のデッキリストを名前のリストと枚数のリストに別々に格納
decklist = csv.reader(open(deckListPath, 'r'), delimiter=' ')
cardNameList = []
cardNumDict = {}
for oneCard in decklist:
	if len(oneCard) < 1 :
		break
	cardNumber = oneCard[0]
	i = 1
	cardName = ''
	while i < len(oneCard): # 空行を読み込んだ時点で終了する <- サイドボードは無視される
		cardName = cardName + oneCard[i] + '+'
		i += 1
	cardNameList.append(cardName)
	cardNumDict[cardName] = cardNumber

# 正規表現の準備
r1 = re.compile('　[A-Z0-9]{3},')  # HTMLからエキスパンションを切り出し
r1_2 = re.compile('[A-Z0-9]{3}') # r1で切り出されたエキスパンションを整形
r2 = re.compile('[0-9]+/[0-9]+\)') # HTMLからコレクター番号を切り出し
r2_2 = re.compile('[0-9]+') # r2で切り出されたコレクター番号を整形

# 各カードについて，名前からエキスパンションとコレクター番号を取得する
#     wisdom-guildに対してURLを発行してwgetでHTMLファイルを取得し，
#     それに対して正規表現でエキスパンションとコレクター番号を切り出し格納する
cardList = []
for cardName in cardNameList:
	print('Obtaining Collector number of', cardName, '...')
	tmpPath = '/tmp/MPP_getCardNum.html'
	url = 'http://whisper.wisdom-guild.net/search.php'
	url += '?name=' + cardName + '&name_op=forward'
	command = ['wget', '-q', '-O', tmpPath, url]
	subprocess.call(command)
	expansionObtainedFlag = 0

	cardExpColnumPair = []
	for line in open(tmpPath, 'r'):
		if(expansionObtainedFlag == 0):
			m = r1.search(line)
		else:
			m = r2.search(line)
		if(m != None):
			if(expansionObtainedFlag == 0):
				expansionObtainedFlag = 1
				m = r1_2.search(m.group(0))
				cardExpColnumPair.append(m.group(0))
			else:
				m = r2_2.match(m.group(0))
				cardExpColnumPair.append(m.group(0))
				cardExpColnumPair.append(cardName)
				cardList.append(cardExpColnumPair)
				break;

# 各カードについて，エキスパンションとコレクター番号から画像ファイルへのパスを生成する
# 複数枚印刷されるカードについては，その分だけパスを発行する．無駄？
cardImgPathList = []
for oneCard in cardList:
	expansion = oneCard[0]
	colNumber = "{0:03d}".format(int(oneCard[1]))
	cardName = oneCard[2]
	cardNum = int(cardNumDict[oneCard[2]])
	for i in range(cardNum):
		if expansion == 'KTK':
			extension = '.png'
		else:
			extension = '.jpg'
		cardImgPathList.append('../img/' + expansion + '/' + colNumber + extension)
	print('print', cardNum, cardName.replace('+', ' '), ':', colNumber, 'of', expansion)

# 上で発行されたパスのリストに対して，それらを全て出力する．
# FIXME: 各画像への処理は関数化した方がすっきり見えると思う
canvasNameCount = 0
while len(cardImgPathList) > 0:
	canvasNameCount += 1
	outDir = '../output/'
	canvasName = outDir + "{0:03d}".format(canvasNameCount) + '.png'
	margin = 10
	cardWidth = 265
	cardHeight = 370
	canvasWidth = margin * 4 + cardWidth * 3
	canvasHeight = margin * 4 + cardHeight * 3
	canvas = Image.new('RGB', (canvasWidth, canvasHeight), (255, 255, 255))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 1 + cardWidth * 0, margin * 1 + cardHeight * 0))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 2 + cardWidth * 1, margin * 1 + cardHeight * 0))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 3 + cardWidth * 2, margin * 1 + cardHeight * 0))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 1 + cardWidth * 0, margin * 2 + cardHeight * 1))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 2 + cardWidth * 1, margin * 2 + cardHeight * 1))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 3 + cardWidth * 2, margin * 2 + cardHeight * 1))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 1 + cardWidth * 0, margin * 3 + cardHeight * 2))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 2 + cardWidth * 1, margin * 3 + cardHeight * 2))

	if len(cardImgPathList) == 0:
		canvas.save(canvasName, 'JPEG', quality=100, optimize=True)
		print('saving', canvasName, '...')
		break;
	cardImgPath = cardImgPathList.pop(0)
	img = Image.open(cardImgPath, 'r')
	img = img.resize((cardWidth, cardHeight))
	canvas.paste(img, (margin * 3 + cardWidth * 2, margin * 3 + cardHeight * 2))

	canvas.save(canvasName, 'PNG', quality=100, optimize=True)
	print('saving', canvasName, '...')

