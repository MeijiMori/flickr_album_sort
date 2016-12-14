# flickr\_album\_sort


##これは何
Flickrのアルバム(フォトセット)のソートを行うプログラムです。  


##使用する前に
このファイルと同じ場所に、api_key.pyとmisc.pyファイルを作成してください。  
api_key.pyには、次の内容を記入してください。  
API\_KEY="FlickrのAPIキー" [必須]  
SECRET\_KEY = "Flickrのシークレットキー" [必須]  

misc.pyには、次の内容を入力してください。  
USER\_ID = "Flickrのユーザーid" [必須]  
IGNORE\_SORT\_ALBUM\_LIST = [  [オプション]
    "ソートを無視したいアルバムid",  
    "ソートを無視したいアルバムid",  
]  
BROWSER\_PATH = "普段使用しているブラウザのパス"  [オプション]  

##使い方
python flickr\_album\_sort.py id                  アルバムのidで昇順にソートを行う  
python flickr\_album\_sort.py title --descending  アルバムのタイトルで降順にソートを行う  
python flickr\_album\_sort.py -d create\_date     アルバムの作成日時で降順にソートを行う  
python flickr\_album\_sort.py -h                  プログラムの使い方を表示する  


##想定環境
使用言語：python 2.7  
必要に応じて、requestsライブラリをインストールして下さい。  
pip install requests  


##作者
Meiji Mori  
