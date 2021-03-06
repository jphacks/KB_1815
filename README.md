# うけトリ

[![Product Name](image.png)](https://www.youtube.com/watch?v=ot3gk7UPOKg&feature=youtu.be)

## 製品概要
### 宅配 × Tech

### 背景（製品開発のきっかけ、課題等）

#### 物流『受け取り方』に変革を
私たちは、物流の最終段階「モノの受け取り方」に注目し、２つの課題を解決します。


#### 「外出していて荷物を受け取れなかった！」
皆さん経験したことあると思います。国土交通省によると、平成30年の4月期だけで、なんと約230万件の再配達が行われたことがわかっています。この再配達は、ドライバー不足問題やCO2排出による環境汚染を引き起こしています。荷物を受け取れない原因は、皆さんと配達員が直接会ってやりとりするという、受け渡しの方法にあるのではないでしょうか。実際、社会生活を営んでいる以上、家で荷物を待つ時間を作るのはなかなか難しいものです。しかし、誰でも利用できるような、外出中に荷物を受け取る手段はほとんどありません。そこで、一般普及率の高いLINEをうまく活かし、家にいなくても荷物を受け取れるようにしたいと考えました。


#### 「ガスが止まってる！？ポストを覗くと、大量のチラシに埋もれて請求書が...一体いつ届いたんだろう...。」
  ポストをちゃんと見てなくて、大事な書類を見落としてしまうこと、ありますよね。大事な郵便物が届いたら、その時に教えて欲しい。宅配と同じく、重要な郵送物の通知もLINEを使えば簡単にできるのでは？と思い、郵送通知機能も持たせる方法を考えました。



### 製品説明（具体的な製品の説明）

#### 宅配うけトリ
- 遠隔操作可能なインターホンと鍵を備えた箱で外出先から宅配物を受け取るシステム。
1. 宅配業者がインターホンを押すと、スピーカーで「誰ですか」と尋ねる。
2. 訪問者が「宅配業者です」と返答後、訪問者の写真と「電話応答をしますか？」という通知が家主にLINEで届く。
  - 「YES」→通話がスタート
  - 「NO」→LINEでテキストを送信し，音声に変換し会話がスタート
3. 支払いが生じる場合は、LINE Payで支払いを完了させる。このとき，LINEにログインすることで，サインの代わりとする。
4. 支払い完了後、家主は開錠のボタンを押し、宅配業者に宅配物を入れてもらい、施錠のボタンを押す。


#### 郵便うけトリ
重要な郵便物が投函されたことを即座に通知するシステム。
1. 郵便物が届くと、カメラが認識する。
2. 重要な封筒とチラシや広告を画像から区別する。
3. 重要な書類の場合、LINEで家主に通知する。（不要な書類は通知しない）

### 特長
1. 配達業者と直接会って荷物を受け取る必要がない。
2. 全ての処理がLINEだけで完結する。
3. 通話ができない場合でも、テキストから音声に変換することで会話ができる。
4. 封筒とチラシや広告を分類し、重要な書類は配達後すぐに知らせてくれる。

### 解決出来ること
再配達の回数が激減する。
重要な書類の見落としを防止する。


### 今後の展望
- 遠隔で家の鍵を操作
　インターフォンから送られる顔写真や音声情報を元に、家族や恋人など、特定の人物を遠隔で家に入れるようにする。

- ブロックチェーンを用いたセキュリティ強化


## 開発内容・開発技術
### 活用した技術

![システム構成](docs/system_detail.png)

#### API・データ

* Line Messaging API
* Line Pay API
* Watson API 
* Google Cloud Text to Speech API

#### フレームワーク・ライブラリ・モジュール
* Node.js
* Express
* Flask
* opencv
* Heroku

#### デバイス
* Raspberry pi
* 外部カメラ
* 外部マイク
* 外部スピーカー
* 光センサー
* スイッチ
* サーボモーター
* カラーボックス

### 研究内容・事前開発プロダクト（任意）
特になし

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* 2日間でアイディアから全て作成しました！
* 郵便物が封筒やハガキなど重要な書類であるか判断し、重要な書類である場合、ユーザーにLINEで通知する仕組み(./src/letter_classifier/pic2type_letter.py)
* ラインを用いて鍵の開け締めを行う機能。
* 遠隔地においても、LINE経由で自宅のインターホンを確認する機能。
* 自宅に居なくても荷物を受け取れる仕組み。
* Line Payによる郵便物の代引き支払い機能。
