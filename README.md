# flickr\_album\_sort


##これは何
Flickrのアルバム(フォトセット)のソートを行うプログラムです。  


##使用する前に
このファイルと同じ場所に、api_key.pyとmisc.pyファイルを作成してください。__
api_key.pyには、次の内容を記入してください。__
API\_KEY="FlickrのAPIキー" [必須]
SECRET\_KEY = "Flickrのシークレットキー" [必須]

misc.pyには、次の内容を入力してください。__
USER\_ID = "Flickrのユーザーid" [必須]
IGNORE\_SORT\_ALBUM\_LIST = [__[オプション]
    "ソートを無視したいアルバムid", _
    "ソートを無視したいアルバムid", _
]__
BROWSER\_PATH = "普段使用しているブラウザのパス"__[オプション]

##使い方
python2 flickr\_album\_sort.py id ascending  アルバムのidで昇順にソートを行う  
python2 flickr\_album\_sort.py title descending  アルバムのタイトルで降順にソートを行う  
python2 flickr\_album\_sort.py create\_date  アルバムの作成日時で昇順にソートを行う  


##想定環境
使用言語：python 2.7  
必要に応じて、requestsライブラリをインストールして下さい。__
pip install requests  


##作者
Meiji Mori
