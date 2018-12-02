# [radvent](https://github.com/nanonanomachine/radvent)の毎日の投稿をslackに通知するツール

```console
$ python src/main.py [アドベントカレンダーのURL] [slackボットのトークン] [アドベントカレンダーのタイトル] [ボットのアイコン] [投稿先チャンネル]
```

使用例：
```console
$ python src/main.py "https://advent.example.com/" "xoxb-000000000-aaaaaaaaaaa" "社内アドベントカレンダー" "http://2.bp.blogspot.com/-yfkaPwPetf8/UYzXG0BwqeI/AAAAAAAAR4g/HLod5E00WNQ/s800/christmas_santa.png" "#general"
```

## 間違って投稿してしまったら

以下で直前1つのメッセージを消せる

```console
$ python src/delete.py [slackボットのトークン] [投稿先チャンネル] [メッセージの一部]
```

使用例：
```console
$ python src/delete.py "xoxb-000000000-aaaaaaaaaaa" "#general" "15日目の記事"
```
