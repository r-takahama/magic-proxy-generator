# MagicProxyPrinter
Magic: the Gatheringの[プロキシ(Proxy)](http://mtgwiki.com/wiki/%E3%83%97%E3%83%AD%E3%82%AD%E3%82%B7)を印刷するための画像を手軽に生成するツール．

**要: python3, wget**

## 対応状況
対応フォーマットは2014/10/11(Sat)現在のスタンダード環境．
対応エキスパンションの一覧は以下

##### [テーロス・ブロック](http://mtgwiki.com/wiki/%E3%83%86%E3%83%BC%E3%83%AD%E3%82%B9%E3%83%BB%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF)
- [テーロス](http://mtgwiki.com/wiki/%E3%83%86%E3%83%BC%E3%83%AD%E3%82%B9) / Theros / THS
- [神々の軍勢](http://mtgwiki.com/wiki/%E7%A5%9E%E3%80%85%E3%81%AE%E8%BB%8D%E5%8B%A2) / Born of the Gods / BNG
- [ニクスへの旅](http://mtgwiki.com/wiki/%E3%83%8B%E3%82%AF%E3%82%B9%E3%81%B8%E3%81%AE%E6%97%85) / Journey into Nyx / JOU

##### [基本セット2015](http://mtgwiki.com/wiki/%E5%9F%BA%E6%9C%AC%E3%82%BB%E3%83%83%E3%83%882015) / Magic Core Set 2015 / M15

##### [タルキール覇王譚ブロック](http://mtgwiki.com/wiki/タルキール覇王譚ブロック)
- [タルキール覇王譚](http://mtgwiki.com/wiki/タルキール覇王譚) / Khans of Tarkir / KTK
	
## 使い方
### ディレクトリ構成
```
MagicProxyPrinter
│	.gitignore
│	README.md
│	
├─decklist
│			testlist.txt
│
├─img
│	│
│	├─BNG
│	│			000.jpg
│	│			...
│	│			165.jpg
│	│
│	├─JOU
│	│			000.jpg
│	│			...
│	│			165.jpg
│	│
│	├─KTK
│	│			001.png
│	│			...
│	│			269.png
│	│
│	├─M15
│	│			001.jpg
│	│			...
│	│			284.jpg
│	│
│	└─THS
│				000.jpg
│				...
│				249.jpg
│
├─output
│			
└─src
			deck2png.py
			downloader.py
```

### 導入方法
適当なディレクトリに移動した後，以下のコマンドを実行する．
```sh
mkdir MagicProxyPrinter
cd MagicProxyPrinter
git clone https://github.com/r-takahama/MagicProxyPrinter.git
mkdir output
```
ここまでで`decklist`, `src`および`output`ディレクトリが生成されているはずである．
しかし，カード画像はGitHubから入手できないため，
**何らかの方法で**`各カードのコレクター番号.jpg`という形式のファイルを入手してくる必要がある(お問い合わせ下さい)．

**何らかの方法で**`img`ディレクトリに正しくファイルを格納した後，MO形式のデッキリストを入手する．
これは，以下のような形式のファイルである．
```
4 Temple of Deceit
4 Temple of Malady
4 Temple of Mystery
1 Mana Confluence
4 Sylvan Caryatid

Sideboard
1 Erebos, God of the Dead
1 Dark Betrayal
```
デッキリストは，`decklist`ディレクトリ以下に保存する．ここで，保存したファイル名を仮に`testlist.txt`とする．

続いて，以下のコマンドを実行する．
```sh
cd src
python deck2png.py
```
ここまでで，`output`ディレクトリ以下にプロキシ画像のファイルが生成される．

この後，各自画像を印刷し，適切な大きさに切り，スリーブに入れプロキシとする．



